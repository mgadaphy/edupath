from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import redis.asyncio as redis
from neo4j import GraphDatabase
import asyncio

from core.config import settings

# PostgreSQL setup
engine = create_engine(
    settings.database_url,
    poolclass=StaticPool,
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis connection
redis_client = None

# Neo4j connection
neo4j_driver = None


async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    return redis_client


def get_neo4j():
    global neo4j_driver
    if neo4j_driver is None:
        neo4j_driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )
    return neo4j_driver


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize all database connections and create tables"""
    print("🔗 Initializing database connections...")
    
    # Create all tables
    from models import student, university, job_market, recommendation
    Base.metadata.create_all(bind=engine)
    
    # Test Redis connection
    try:
        redis_conn = await get_redis()
        await redis_conn.ping()
        print("✅ Redis connection established")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
    
    # Test Neo4j connection
    try:
        driver = get_neo4j()
        driver.verify_connectivity()
        print("✅ Neo4j connection established")
        
        # Initialize knowledge graph schema
        await init_knowledge_graph()
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
    
    print("✅ Database initialization completed")


async def init_knowledge_graph():
    """Initialize the knowledge graph with basic structure"""
    driver = get_neo4j()
    
    with driver.session() as session:
        # Create constraints and indexes
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Subject) REQUIRE s.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Program) REQUIRE p.code IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (u:University) REQUIRE u.code IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Career) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (sk:Skill) REQUIRE sk.name IS UNIQUE",
        ]
        
        for constraint in constraints:
            try:
                session.run(constraint)
            except Exception:
                pass  # Constraint may already exist
        
        print("✅ Knowledge graph schema initialized")


async def close_connections():
    """Close all database connections"""
    global redis_client, neo4j_driver
    
    if redis_client:
        await redis_client.close()
    
    if neo4j_driver:
        neo4j_driver.close()
