import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const UniversitiesPage: React.FC = () => {
  return (
    <div className="container mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Universities</CardTitle>
          <CardDescription>Explore universities and programs</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">University listings coming soon...</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default UniversitiesPage;
