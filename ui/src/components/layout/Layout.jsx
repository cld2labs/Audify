import { Outlet } from 'react-router-dom';
import Footer from './Footer';
import { RippleBackground } from '../ui';
import { ResizableNavbar } from './ResizableNavbar';

export const Layout = () => {
  return (
    <div className="flex flex-col min-h-screen relative bg-neutral-50">
      <div className="fixed inset-0 z-0">
        {/* pointer-events-none mostly, but we want interaction? 
             If we want interaction, we need pointer-events-auto but z-index -1? 
             If z-0 is behind content (z-10), clicks on content won't hit it. 
             Clicks on whitespace will. 
             But header/main/footer need to be distinct.
          */}
        <RippleBackground className="w-full h-full" />
      </div>

      {/* Content wrapper with z-index to sit above background */}
      <div className="relative z-10 flex flex-col min-h-screen">
        <ResizableNavbar />
        {/* Added top padding to account for fixed navbar */}
        <main className="flex-1 container mx-auto px-4 sm:px-6 lg:px-8 py-8 mt-24">
          <Outlet />
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default Layout;
