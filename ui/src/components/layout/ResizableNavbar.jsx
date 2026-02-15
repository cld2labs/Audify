import React, { useState } from "react";
import {
    motion,
    AnimatePresence,
    useScroll,
    useMotionValueEvent,
} from "framer-motion";
import { Link, useLocation } from "react-router-dom";
import clsx from "clsx";
import { Mic2, Home, FolderKanban, Settings, Menu, X } from "lucide-react";

export const ResizableNavbar = ({ className }) => {
    const { scrollY } = useScroll();
    const [scrolled, setScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const location = useLocation();

    useMotionValueEvent(scrollY, "change", (latest) => {
        setScrolled(latest > 50);
    });

    const navItems = [
        { name: "Home", link: "/", icon: <Home className="w-4 h-4" /> },
        { name: "Generate", link: "/generate", icon: <Mic2 className="w-4 h-4" /> },
        { name: "Projects", link: "/projects", icon: <FolderKanban className="w-4 h-4" /> },
        { name: "Settings", link: "/settings", icon: <Settings className="w-4 h-4" /> },
    ];

    return (
        <div
            className={clsx(
                "fixed top-0 inset-x-0 z-50 flex justify-center pt-4",
                className
            )}
        >
            <motion.nav
                initial={{
                    width: "90%",
                    borderRadius: "1rem",
                }}
                animate={{
                    width: scrolled ? "50%" : "90%",
                    borderRadius: scrolled ? "2rem" : "1rem",
                }}
                transition={{
                    type: "spring",
                    stiffness: 260,
                    damping: 20,
                }}
                className={clsx(
                    "relative flex items-center justify-between px-6 py-3 shadow-lg border backdrop-blur-md transition-colors duration-300",
                    scrolled
                        ? "bg-primary-950/90 border-primary-800 text-white"
                        : "bg-white/90 border-neutral-200 text-neutral-800"
                )}
            >
                {/* Logo Section */}
                <Link to="/" className="flex items-center gap-2 font-bold text-lg whitespace-nowrap">
                    <img
                        src="/cloud2labs-logo.png"
                        alt="Logo"
                        className="h-8 w-auto object-contain"
                    />
                    <span className={clsx("hidden sm:block", scrolled ? "text-white" : "text-primary-900")}>
                        Audify
                    </span>
                </Link>

                {/* Desktop Nav Items */}
                <div className="hidden md:flex flex-1 items-center justify-center gap-1">
                    {navItems.map((item) => {
                        const isActive = location.pathname === item.link;
                        return (
                            <Link
                                key={item.name}
                                to={item.link}
                                className={clsx(
                                    "relative px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 flex items-center gap-2",
                                    isActive
                                        ? (scrolled ? "bg-primary-800 text-white" : "bg-primary-100 text-primary-900")
                                        : (scrolled ? "hover:bg-primary-800/50 text-neutral-300 hover:text-white" : "hover:bg-neutral-100 text-neutral-600 hover:text-neutral-900")
                                )}
                            >
                                {item.icon}
                                <span>{item.name}</span>
                            </Link>
                        )
                    })}
                </div>

                {/* Mobile Toggle */}
                <button
                    onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    className="md:hidden p-2 rounded-full hover:bg-neutral-100/10"
                >
                    {mobileMenuOpen
                        ? <X className={clsx("w-5 h-5", scrolled ? "text-white" : "text-neutral-800")} />
                        : <Menu className={clsx("w-5 h-5", scrolled ? "text-white" : "text-neutral-800")} />
                    }
                </button>

                {/* Action Button (Placeholder for right side, e.g. Profile or CTA) */}
                <div className="hidden md:block w-[100px] flex justify-end">
                    {/* Can add User Profile here later */}
                </div>

            </motion.nav>

            {/* Mobile Menu Dropdown */}
            <AnimatePresence>
                {mobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="absolute top-20 left-4 right-4 bg-white rounded-2xl shadow-xl border border-neutral-200 p-4 flex flex-col gap-2 md:hidden"
                    >
                        {navItems.map((item) => (
                            <Link
                                key={item.name}
                                to={item.link}
                                onClick={() => setMobileMenuOpen(false)}
                                className={clsx(
                                    "flex items-center gap-3 px-4 py-3 rounded-xl transition-colors",
                                    location.pathname === item.link
                                        ? "bg-primary-50 text-primary-700 font-semibold"
                                        : "hover:bg-neutral-50 text-neutral-600"
                                )}
                            >
                                {item.icon}
                                {item.name}
                            </Link>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
