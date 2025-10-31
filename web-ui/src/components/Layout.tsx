import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  FileText, 
  Clock, 
  Camera,
  Activity
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/concepts', icon: FileText, label: 'Concepts' },
    { path: '/timeline', icon: Clock, label: 'Timeline' },
    { path: '/snapshots', icon: Camera, label: 'Snapshots' },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="w-8 h-8 text-panini-blue" />
              <div>
                <h1 className="text-2xl font-bold text-white">Panini-FS</h1>
                <p className="text-sm text-gray-400">Temporal Filesystem</p>
              </div>
            </div>
            
            <nav className="flex space-x-1">
              {navItems.map(({ path, icon: Icon, label }) => (
                <Link
                  key={path}
                  to={path}
                  className={`
                    flex items-center space-x-2 px-4 py-2 rounded-lg
                    transition-colors duration-200
                    ${isActive(path)
                      ? 'bg-panini-blue text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{label}</span>
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 mt-auto">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between text-sm text-gray-400">
            <p>Panini-FS v2.0 - Immutable Time-Travel Filesystem</p>
            <p>Built with ❤️ using Rust + React</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
