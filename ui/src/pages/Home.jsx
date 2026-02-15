import { Link } from 'react-router-dom';
import { Upload, Sparkles, Download, ArrowRight, ChevronRight } from 'lucide-react';
import { Button, FocusCards, HoverEffect } from '@components/ui';
import { cn } from '@utils/helpers';

export const Home = () => {
  const features = [
    {
      icon: <Upload className="w-6 h-6" />,
      title: 'Easy Upload',
      description: 'Simply drag and drop your document to get started',
    },
    {
      icon: <Sparkles className="w-6 h-6" />,
      title: 'AI-Powered',
      description: 'Advanced AI creates natural, engaging podcast conversations',
    },
    {
      icon: <Download className="w-6 h-6" />,
      title: 'Multiple Voices',
      description: 'Choose from 6 professional AI voices for host and guest',
    },
    {
      icon: <Download className="w-6 h-6" />,
      title: 'Download & Share',
      description: 'Get high-quality MP3 audio ready to share anywhere',
    },
  ];

  const steps = [
    {
      number: 1,
      title: 'Upload Document',
      description: 'Upload your document (max 10MB)',
    },
    {
      number: 2,
      title: 'Select Voices',
      description: 'Choose AI voices for host and guest',
    },
    {
      number: 3,
      title: 'Review Script',
      description: 'Edit the generated conversation if needed',
    },
    {
      number: 4,
      title: 'Download',
      description: 'Get your Podcast audio file',
    },
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <div className="inline-block">
          {/* Custom Hero Image - Replace src with your actual image */}
          <img
            src="/hero-image-removebg-preview.png"
            alt="Audify"
            className="w-48 h-48 object-contain mx-auto mb-6"
            onError={(e) => {
              // Fallback to gradient box if image not found
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'inline-block';
            }}
          />
          <div
            className="bg-gradient-to-br from-primary-600 to-secondary-600 p-4 rounded-2xl mb-6 shadow-xl"
            style={{ display: 'none' }}
          >
            <div className="w-40 h-40 bg-white rounded-lg" />
          </div>
        </div>

        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight">
          Transform Document into
          <br />
          <span className="bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
            Engaging Podcasts
          </span>
        </h1>

        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Turn any document into a natural, AI-powered Podcast conversation
          in minutes. Perfect for learning, content creation, and accessibility.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Link to="/generate">
            <Button size="xl" icon={ArrowRight} iconPosition="right">
              Get Started
            </Button>
          </Link>
          <Link to="/projects">
            <Button size="xl" variant="outline">
              View Projects
            </Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section>
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Why Choose Audify?
        </h2>
        <FocusCards cards={features} />
      </section>

      {/* How It Works */}
      <section>
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">
          How It Works
        </h2>

        <HoverEffect items={steps} />
      </section>

      {/* CTA */}
      {/* CTA */}
      <section className="bg-neutral-700 rounded-2xl p-12 text-center text-white shadow-2xl border border-neutral-800 relative overflow-hidden">
        {/* Subtle decorative circle */}
        <div className="absolute top-0 right-0 -mt-20 -mr-20 w-80 h-80 bg-neutral-900 rounded-full blur-3xl opacity-50 pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-80 h-80 bg-neutral-900 rounded-full blur-3xl opacity-50 pointer-events-none"></div>

        <div className="relative z-10">
          <h2 className="text-3xl md:text-4xl font-bold mb-6 tracking-tight">
            Ready to Create Your First Podcast?
          </h2>
          <p className="text-xl mb-10 text-neutral-200 max-w-2xl mx-auto">
            Get started in less than 5 minutes. No sign-up required.
          </p>
          <Link to="/generate">
            <Button size="xl" variant="secondary" className="font-bold px-8">
              Start Generating Now
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
