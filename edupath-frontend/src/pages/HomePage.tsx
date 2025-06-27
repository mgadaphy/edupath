import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  GraduationCap, 
  Target, 
  BookOpen, 
  Users, 
  TrendingUp, 
  Lightbulb,
  ArrowRight,
  CheckCircle,
  Star,
  Globe
} from 'lucide-react';
import { useSession } from '@/contexts/SessionContext';

const HomePage: React.FC = () => {
  const { language, sessionId } = useSession();

  const features = [
    {
      icon: Target,
      title: language === 'en' ? 'Personalized Recommendations' : 'Recommandations Personnalisées',
      description: language === 'en' 
        ? 'AI-powered analysis of your academic performance to suggest the best university programs'
        : 'Analyse IA de vos performances académiques pour suggérer les meilleurs programmes universitaires'
    },
    {
      icon: BookOpen,
      title: language === 'en' ? 'Dual Education Systems' : 'Systèmes Éducatifs Duaux',
      description: language === 'en'
        ? 'Support for both GCE (O/A Level) and French (BEPC/Baccalauréat) educational systems'
        : 'Support pour les systèmes GCE (O/A Level) et français (BEPC/Baccalauréat)'
    },
    {
      icon: TrendingUp,
      title: language === 'en' ? 'Job Market Insights' : 'Aperçus du Marché du Travail',
      description: language === 'en'
        ? 'Real-time analysis of career opportunities and employment trends in Cameroon'
        : 'Analyse en temps réel des opportunités de carrière et tendances d\'emploi au Cameroun'
    },
    {
      icon: Users,
      title: language === 'en' ? 'Multi-Agent AI System' : 'Système IA Multi-Agents',
      description: language === 'en'
        ? 'Sophisticated AI agents working together to provide comprehensive guidance'
        : 'Agents IA sophistiqués travaillant ensemble pour fournir des conseils complets'
    },
    {
      icon: Globe,
      title: language === 'en' ? 'Bilingual Support' : 'Support Bilingue',
      description: language === 'en'
        ? 'Full support for English and French, respecting Cameroon\'s bilingual nature'
        : 'Support complet en anglais et français, respectant la nature bilingue du Cameroun'
    },
    {
      icon: Lightbulb,
      title: language === 'en' ? 'AI-Generated Content' : 'Contenu Généré par IA',
      description: language === 'en'
        ? 'Personalized study guides, career advice, and preparation tips using Google Gemini'
        : 'Guides d\'étude personnalisés, conseils de carrière et astuces de préparation avec Google Gemini'
    }
  ];

  const stats = [
    { number: '3+', label: language === 'en' ? 'Major Universities' : 'Universités Principales' },
    { number: '15+', label: language === 'en' ? 'Study Programs' : 'Programmes d\'Études' },
    { number: '10+', label: language === 'en' ? 'Career Sectors' : 'Secteurs de Carrière' },
    { number: '2', label: language === 'en' ? 'Education Systems' : 'Systèmes Éducatifs' }
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center space-y-8">
        <div className="space-y-4">
          <div className="mb-4 inline-flex items-center rounded-md border border-transparent bg-secondary px-2.5 py-0.5 text-xs font-semibold text-secondary-foreground transition-colors hover:bg-secondary/80">
            {language === 'en' ? '🇨🇲 Made for Cameroon' : '🇨🇲 Fait pour le Cameroun'}
          </div>
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-green-600 bg-clip-text text-transparent">
            {language === 'en' ? 'Your Guide to Academic Success' : 'Votre Guide vers le Succès Académique'}
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            {language === 'en' 
              ? 'Discover the perfect university program and career path tailored to your academic strengths and interests using advanced AI technology.'
              : 'Découvrez le programme universitaire et le parcours professionnel parfaits adaptés à vos forces académiques et intérêts grâce à la technologie IA avancée.'
            }
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link to={sessionId ? "/profile" : "/profile"}>
            <Button className="h-12 rounded-md bg-gradient-to-r from-blue-600 to-green-600 hover:from-blue-700 hover:to-green-700 text-white px-8 py-3">
              <GraduationCap className="mr-2 h-5 w-5" />
              {language === 'en' ? 'Get Started' : 'Commencer'}
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
          <Link to="/about">
            <Button variant="outline" size="lg" className="px-8 py-3">
              {language === 'en' ? 'Learn More' : 'En Savoir Plus'}
            </Button>
          </Link>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-12">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-3xl font-bold text-blue-600">{stat.number}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="space-y-8">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold">
            {language === 'en' ? 'Intelligent Features' : 'Fonctionnalités Intelligentes'}
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            {language === 'en'
              ? 'Our AI-powered platform combines multiple specialized agents to provide comprehensive educational guidance.'
              : 'Notre plateforme IA combine plusieurs agents spécialisés pour fournir des conseils éducatifs complets.'
            }
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-green-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-blue-600" />
                </div>
                <CardTitle className="text-lg">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600 leading-relaxed">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="space-y-8">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold">
            {language === 'en' ? 'How EduPath Works' : 'Comment EduPath Fonctionne'}
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            {language === 'en'
              ? 'Simple steps to discover your ideal academic and career path'
              : 'Étapes simples pour découvrir votre parcours académique et professionnel idéal'
            }
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              step: '01',
              title: language === 'en' ? 'Create Profile' : 'Créer un Profil',
              description: language === 'en' 
                ? 'Enter your academic results (GCE or French system) and personal interests'
                : 'Entrez vos résultats académiques (GCE ou système français) et intérêts personnels'
            },
            {
              step: '02',
              title: language === 'en' ? 'AI Analysis' : 'Analyse IA',
              description: language === 'en'
                ? 'Our multi-agent AI system analyzes your profile against university requirements and job market data'
                : 'Notre système IA multi-agents analyse votre profil par rapport aux exigences universitaires et données du marché du travail'
            },
            {
              step: '03',
              title: language === 'en' ? 'Get Recommendations' : 'Obtenir des Recommandations',
              description: language === 'en'
                ? 'Receive personalized university program suggestions with career guidance and preparation tips'
                : 'Recevez des suggestions de programmes universitaires personnalisées avec des conseils de carrière et de préparation'
            }
          ].map((item, index) => (
            <Card key={index} className="text-center hover:shadow-lg transition-shadow duration-300">
              <CardHeader>
                <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold text-xl">{item.step}</span>
                </div>
                <CardTitle>{item.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="leading-relaxed">
                  {item.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-blue-600 to-green-600 rounded-2xl p-8 md:p-12 text-center text-white">
        <div className="space-y-6">
          <h2 className="text-3xl md:text-4xl font-bold">
            {language === 'en' ? 'Ready to Start Your Journey?' : 'Prêt à Commencer Votre Parcours?'}
          </h2>
          <p className="text-xl opacity-90 max-w-2xl mx-auto">
            {language === 'en'
              ? 'Join thousands of Cameroonian students discovering their perfect academic path with AI-powered guidance.'
              : 'Rejoignez des milliers d\'étudiants camerounais découvrant leur parcours académique parfait avec des conseils IA.'
            }
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/profile">
              <Button size="lg" variant="secondary" className="px-8 py-3">
                <Star className="mr-2 h-5 w-5" />
                {language === 'en' ? 'Start Free Assessment' : 'Commencer l\'Évaluation Gratuite'}
              </Button>
            </Link>
            <Link to="/universities">
              <Button 
                size="lg" 
                variant="outline-blue"
                className="px-8 py-3"
              >
                {language === 'en' ? 'Explore Universities' : 'Explorer les Universités'}
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
