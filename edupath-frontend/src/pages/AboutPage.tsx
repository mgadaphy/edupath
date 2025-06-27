import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, GraduationCap, Lightbulb, Users, Heart, Award, Globe } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, children }: { icon: React.ElementType, title: string, children: React.ReactNode }) => (
  <div className="flex flex-col items-center text-center p-6 rounded-lg border bg-card">
    <div className="p-3 mb-4 rounded-full bg-primary/10">
      <Icon className="h-8 w-8 text-primary" />
    </div>
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <p className="text-muted-foreground">{children}</p>
  </div>
);

const AboutPage: React.FC = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <div className="container mx-auto py-8 space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-4 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">Empowering Cameroon's Future Through Education</h1>
        <p className="text-xl text-muted-foreground">
          EduPath is an AI-powered platform that helps Cameroonian students discover their ideal career paths and 
          navigate the complex landscape of higher education opportunities.
        </p>
      </div>

      {/* Mission Section */}
      <section className="space-y-6">
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-4">Our Mission</h2>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
            To bridge the gap between Cameroonian students and their educational aspirations by providing 
            personalized guidance, comprehensive resources, and data-driven insights to make informed decisions 
            about their academic and professional futures.
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section className="space-y-8">
        <h2 className="text-3xl font-bold text-center">What We Offer</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <FeatureCard icon={GraduationCap} title="Personalized Career Guidance">
            AI-powered career recommendations based on your skills, interests, and academic performance.
          </FeatureCard>
          <FeatureCard icon={BookOpen} title="Comprehensive University Database">
            Detailed information about universities, programs, admission requirements, and more across Cameroon.
          </FeatureCard>
          <FeatureCard icon={Lightbulb} title="Skill Assessment" >
            Identify your strengths and areas for improvement with our interactive assessment tools.
          </FeatureCard>
          <FeatureCard icon={Award} title="Scholarship Opportunities">
            Discover funding opportunities and scholarships tailored to your profile.
          </FeatureCard>
          <FeatureCard icon={Globe} title="Career Pathways" >
            Explore various career options and the educational paths that lead to them.
          </FeatureCard>
          <FeatureCard icon={Users} title="Mentorship Network">
            Connect with professionals and alumni for guidance and advice.
          </FeatureCard>
        </div>
      </section>

      {/* Team Section */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold text-center">Our Team</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <div className="h-32 w-32 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Users className="h-16 w-16 text-primary" />
              </div>
              <CardTitle className="text-center">Mo Gadaphy</CardTitle>
              <CardDescription className="text-center">Founder & Lead Developer</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-sm text-muted-foreground">
                Education technology enthusiast with a passion for making quality education accessible to all.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <div className="h-32 w-32 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Users className="h-16 w-16 text-primary" />
              </div>
              <CardTitle className="text-center">MOGADONKO AGENCY</CardTitle>
              <CardDescription className="text-center">Development Partner</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-sm text-muted-foreground">
                A team of dedicated professionals committed to building innovative technology solutions.
              </p>
              <a 
                href="https://mogadonko.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:underline mt-2 inline-block"
              >
                Visit mogadonko.com
              </a>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <div className="h-32 w-32 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Heart className="h-16 w-16 text-primary" />
              </div>
              <CardTitle className="text-center">Our Community</CardTitle>
              <CardDescription className="text-center">You Make the Difference</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-sm text-muted-foreground">
                Special thanks to all the educators, students, and professionals who contribute to making EduPath better every day.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Contact CTA */}
      <section className="bg-primary/5 rounded-lg p-8 text-center">
        <h2 className="text-2xl font-bold mb-4">Have Questions?</h2>
        <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
          We're here to help you on your educational journey. Reach out to us for support or partnership opportunities.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a 
            href="mailto:contact@edupath.cm" 
            className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary hover:bg-primary/90"
          >
            Contact Us
          </a>
          <a 
            href="https://github.com/mgadaphy/edupath" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            View on GitHub
          </a>
        </div>
      </section>

      {/* Footer Note */}
      <div className="text-center text-sm text-muted-foreground pt-8 border-t">
        <p>© {currentYear} EduPath. All rights reserved. A project by Mo Gadaphy & MOGADONKO AGENCY.</p>
        <p className="mt-2">
          Made with <span className="text-red-500">❤</span> in Cameroon
        </p>
      </div>
    </div>
  );
};

export default AboutPage;
