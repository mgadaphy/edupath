import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const AboutPage: React.FC = () => {
  return (
    <div className="container mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>About EduPath</CardTitle>
          <CardDescription>Your AI-powered educational guidance system</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            EduPath helps Cameroonian students discover their ideal career paths and educational opportunities.
          </p>
          <div className="space-y-2">
            <h3 className="font-semibold">Features:</h3>
            <ul className="list-disc pl-6 space-y-1 text-muted-foreground">
              <li>Personalized career recommendations</li>
              <li>University and program exploration</li>
              <li>Skill assessment and gap analysis</li>
              <li>Scholarship and funding opportunities</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AboutPage;
