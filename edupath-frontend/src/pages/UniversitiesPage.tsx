import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Building2, MapPin, Globe, BookOpen, GraduationCap, Users, Clock } from 'lucide-react';

// Import university data
import universityData from '@/data/universities';

interface Program {
  code: string;
  name: string;
  name_fr: string;
  degree_type: string;
  duration_years: number;
  faculty: string;
  department: string;
  description?: string;
  career_prospects?: string[];
  tuition_fee_fcfa?: number;
  language_instruction?: string;
  is_competitive?: boolean;
  entrance_exam_required?: boolean;
}

interface University {
  id: string;
  name: string;
  name_fr: string;
  acronym: string;
  location: string;
  location_fr: string;
  website: string;
  logo: string;
  description: string;
  description_fr: string;
  programs: Program[];
}

const UniversitiesPage: React.FC = () => {
  const [universities, setUniversities] = useState<University[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('');

  useEffect(() => {
    // In a real app, you would fetch this from an API
    setUniversities(universityData as unknown as University[]);
    if (universityData.length > 0) {
      setActiveTab(universityData[0].id);
    }
    setLoading(false);
  }, []);

  const renderProgramCard = (program: Program) => (
    <div key={program.code} className="mb-6 p-4 border rounded-lg hover:bg-accent/50 transition-colors">
      <div className="flex justify-between items-start">
        <div>
          <h4 className="font-semibold text-lg">{program.name}</h4>
          <p className="text-sm text-muted-foreground">{program.faculty} • {program.department}</p>
          
          <div className="mt-2 flex flex-wrap gap-2">
            <Badge variant="outline" className="flex items-center gap-1">
              <span className="text-xs">{program.degree_type.toUpperCase()}</span>
            </Badge>
            <Badge variant="outline" className="flex items-center gap-1">
              <span className="text-xs">{program.duration_years} years</span>
            </Badge>
            {program.is_competitive && (
              <Badge variant="secondary">Competitive</Badge>
            )}
            {program.entrance_exam_required && (
              <Badge variant="outline">Entrance Exam</Badge>
            )}
          </div>
          
          {program.tuition_fee_fcfa && (
            <div className="mt-2">
              <span className="text-sm font-medium">Tuition: </span>
              <span className="text-sm">{program.tuition_fee_fcfa.toLocaleString()} FCFA/year</span>
            </div>
          )}
        </div>
      </div>
      
      {program.description && (
        <p className="mt-2 text-sm">{program.description}</p>
      )}
      
      {program.career_prospects && program.career_prospects.length > 0 && (
        <div className="mt-2">
          <p className="text-sm font-medium">Career Prospects:</p>
          <div className="flex flex-wrap gap-1 mt-1">
            {program.career_prospects.map((prospect, i) => (
              <Badge key={i} variant="outline" className="text-xs">
                <span className="text-xs">{prospect}</span>
              </Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <Card>
          <CardHeader>
            <CardTitle>Loading Universities...</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">Please wait while we load the university data.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Cameroon Universities</h1>
        <p className="text-muted-foreground mt-2">
          Explore universities and programs across Cameroon to find your perfect academic path.
        </p>
      </div>

      <Tabs defaultValue={activeTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 md:grid-cols-4 lg:grid-cols-6 mb-6">
          {universities.map((university) => (
            <TabsTrigger 
              key={university.id} 
              value={university.id}
              className="flex flex-col items-center h-auto py-2"
            >
              <Building2 className="h-5 w-5 mb-1" />
              <span className="text-xs mt-1 text-center">{university.acronym}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {universities.map((university) => (
          <TabsContent key={university.id} value={university.id} className="space-y-6">
            <Card>
              <CardHeader className="pb-4">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-3">
                      <img 
                        src={university.logo} 
                        alt={`${university.name} logo`} 
                        className="h-12 w-12 object-contain"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.style.display = 'none';
                        }}
                      />
                      <div>
                        <CardTitle className="text-2xl">{university.name}</CardTitle>
                        <div className="flex items-center text-sm text-muted-foreground mt-1">
                          <MapPin className="h-4 w-4 mr-1" />
                          {university.location}
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-3 flex flex-wrap gap-2">
                      <a 
                        href={university.website} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-blue-600 hover:underline"
                      >
                        <Globe className="h-4 w-4 mr-1" />
                        Visit Website
                      </a>
                    </div>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold mb-2">About</h3>
                    <p className="text-muted-foreground">{university.description}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                      <BookOpen className="h-5 w-5 mr-2" />
                      Academic Programs
                    </h3>
                    
                    <div className="space-y-4">
                      {university.programs.length > 0 ? (
                        university.programs.map(renderProgramCard)
                      ) : (
                        <p className="text-muted-foreground italic">No program information available.</p>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
};

export default UniversitiesPage;
