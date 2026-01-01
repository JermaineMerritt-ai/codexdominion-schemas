/**
 * WORKFLOW CATALOG CARD - WEBSITE CREATION
 * ==========================================
 * React component for displaying website creation workflow in the catalog
 */

import React from 'react';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Globe, 
  Clock, 
  DollarSign, 
  CheckCircle, 
  AlertTriangle,
  Sparkles,
  ArrowRight
} from 'lucide-react';

interface WorkflowCardProps {
  onSelect?: () => void;
  featured?: boolean;
}

export const WebsiteCreationWorkflowCard: React.FC<WorkflowCardProps> = ({ 
  onSelect,
  featured = false 
}) => {
  return (
    <Card className={`
      relative overflow-hidden transition-all duration-300 hover:shadow-lg
      ${featured ? 'border-2 border-amber-400 ring-2 ring-amber-400/20' : 'border-stone-200'}
    `}>
      {/* Featured Badge */}
      {featured && (
        <div className="absolute top-4 right-4 z-10">
          <Badge className="bg-amber-400 text-stone-900 font-semibold">
            <Sparkles className="w-3 h-3 mr-1" />
            POPULAR
          </Badge>
        </div>
      )}

      <CardHeader className="space-y-3">
        {/* Icon + Title */}
        <div className="flex items-start gap-3">
          <div className="p-3 rounded-lg bg-stone-100 text-stone-800">
            <Globe className="w-6 h-6" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-bold text-stone-900">
              Create Basic Website
            </h3>
            <p className="text-sm text-stone-600 mt-1">
              Professional starter site with SEO, branding, and deployment
            </p>
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2">
          <Badge variant="outline" className="text-xs">
            <Globe className="w-3 h-3 mr-1" />
            Next.js 14
          </Badge>
          <Badge variant="outline" className="text-xs bg-green-50 text-green-700 border-green-200">
            <CheckCircle className="w-3 h-3 mr-1" />
            Auto-Deploy
          </Badge>
          <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200">
            Media Council
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Key Metrics */}
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-3 rounded-lg bg-stone-50">
            <Clock className="w-4 h-4 mx-auto mb-1 text-stone-600" />
            <div className="text-2xl font-bold text-stone-900">15</div>
            <div className="text-xs text-stone-600">minutes</div>
          </div>
          <div className="text-center p-3 rounded-lg bg-green-50">
            <DollarSign className="w-4 h-4 mx-auto mb-1 text-green-600" />
            <div className="text-2xl font-bold text-green-700">$225</div>
            <div className="text-xs text-green-600">saved</div>
          </div>
          <div className="text-center p-3 rounded-lg bg-amber-50">
            <Sparkles className="w-4 h-4 mx-auto mb-1 text-amber-600" />
            <div className="text-2xl font-bold text-amber-700">5+</div>
            <div className="text-xs text-amber-600">pages</div>
          </div>
        </div>

        {/* What's Included */}
        <div className="space-y-2">
          <h4 className="text-sm font-semibold text-stone-900">What's Included:</h4>
          <ul className="space-y-1.5">
            {[
              'Home, About, Contact, Blog pages',
              'SEO metadata (sitemap, meta tags)',
              'Mobile-responsive design',
              'Contact form integration',
              'Brand colors & typography',
              'GitHub repository + live URL'
            ].map((item, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-stone-700">
                <CheckCircle className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Governance Info */}
        <div className="p-3 rounded-lg bg-blue-50 border border-blue-200">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-xs font-medium text-blue-900">Requires Review</p>
              <p className="text-xs text-blue-700 mt-0.5">
                Media Council reviews for brand consistency and SEO best practices
              </p>
            </div>
          </div>
        </div>

        {/* ROI Breakdown */}
        <div className="p-3 rounded-lg bg-stone-50 border border-stone-200">
          <h4 className="text-xs font-semibold text-stone-900 mb-2">Savings Breakdown:</h4>
          <div className="space-y-1 text-xs text-stone-700">
            <div className="flex justify-between">
              <span>Manual creation time:</span>
              <span className="font-medium">3 hours</span>
            </div>
            <div className="flex justify-between">
              <span>Developer rate:</span>
              <span className="font-medium">$75/hour</span>
            </div>
            <div className="flex justify-between">
              <span>Error reduction:</span>
              <span className="font-medium text-green-600">85%</span>
            </div>
            <div className="flex justify-between pt-1 border-t border-stone-300 font-semibold">
              <span>Total annual value:</span>
              <span className="text-green-600">$11,700</span>
            </div>
          </div>
        </div>
      </CardContent>

      <CardFooter className="flex gap-2">
        <Button 
          onClick={onSelect}
          className="flex-1 bg-stone-900 hover:bg-stone-800 text-white"
        >
          Create Website
          <ArrowRight className="w-4 h-4 ml-2" />
        </Button>
        <Button 
          variant="outline"
          className="border-stone-300 hover:bg-stone-50"
        >
          View Details
        </Button>
      </CardFooter>

      {/* Bottom accent line */}
      <div className="h-1 bg-gradient-to-r from-amber-400 via-stone-800 to-amber-400" />
    </Card>
  );
};


/**
 * GRID VIEW VARIANT - Compact card for catalog grid
 */
export const WebsiteCreationWorkflowCardCompact: React.FC<WorkflowCardProps> = ({ 
  onSelect 
}) => {
  return (
    <Card className="hover:shadow-md transition-all cursor-pointer" onClick={onSelect}>
      <CardHeader className="pb-3">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-stone-100">
            <Globe className="w-5 h-5 text-stone-800" />
          </div>
          <div className="flex-1">
            <h4 className="font-semibold text-stone-900 text-sm">Basic Website</h4>
            <p className="text-xs text-stone-600">Next.js • Auto-deploy</p>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-stone-600">Duration</span>
          <span className="font-medium text-stone-900">15 min</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-stone-600">Savings</span>
          <span className="font-medium text-green-600">$225</span>
        </div>
        <Badge variant="outline" className="w-full justify-center text-xs">
          Media Council
        </Badge>
      </CardContent>
    </Card>
  );
};


/**
 * USAGE EXAMPLE
 */
export const WorkflowCatalogExample = () => {
  const handleSelectWorkflow = () => {
    console.log('Opening workflow creation form...');
    // Navigate to workflow creation or open modal
  };

  return (
    <div className="p-8 bg-stone-50 min-h-screen">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-stone-900">Workflow Catalog</h1>
          <p className="text-stone-600 mt-2">
            Automated workflows to accelerate your digital empire
          </p>
        </div>

        {/* Featured Section */}
        <div>
          <h2 className="text-xl font-semibold text-stone-900 mb-4">Featured Workflows</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <WebsiteCreationWorkflowCard 
              onSelect={handleSelectWorkflow}
              featured={true}
            />
            {/* Other featured workflows */}
          </div>
        </div>

        {/* All Workflows Grid */}
        <div>
          <h2 className="text-xl font-semibold text-stone-900 mb-4">All Workflows</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <WebsiteCreationWorkflowCardCompact onSelect={handleSelectWorkflow} />
            {/* Other workflows */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WebsiteCreationWorkflowCard;
