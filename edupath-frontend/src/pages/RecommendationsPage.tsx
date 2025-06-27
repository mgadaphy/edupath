import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const RecommendationsPage: React.FC = () => {
  return (
    <div className="container mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Career Recommendations</CardTitle>
          <CardDescription>View your personalized career recommendations</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Recommendations will appear here based on your profile and assessments.</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default RecommendationsPage;
