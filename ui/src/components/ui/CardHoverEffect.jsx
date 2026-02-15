import { cn } from "@utils/helpers";
import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";

export const HoverEffect = ({ items, className }) => {
    let [hoveredIndex, setHoveredIndex] = useState(null);

    return (
        <div
            className={cn(
                "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 py-6",
                className
            )}
        >
            {items.map((item, idx) => (
                <div
                    key={idx}
                    className="relative group block p-2 h-full w-full"
                    onMouseEnter={() => setHoveredIndex(idx)}
                    onMouseLeave={() => setHoveredIndex(null)}
                >
                    <AnimatePresence>
                        {hoveredIndex === idx && (
                            <motion.span
                                className="absolute inset-0 h-full w-full bg-primary-100 block rounded-3xl"
                                layoutId="hoverBackground"
                                initial={{ opacity: 0 }}
                                animate={{
                                    opacity: 1,
                                    transition: { duration: 0.15 },
                                }}
                                exit={{
                                    opacity: 0,
                                    transition: { duration: 0.15, delay: 0.2 },
                                }}
                            />
                        )}
                    </AnimatePresence>
                    <Card>
                        <div className="flex flex-col h-full bg-white rounded-2xl p-4 shadow-sm relative z-20">
                            <div className="w-10 h-10 rounded-full bg-primary-50 flex items-center justify-center mb-4">
                                <span className="font-bold text-primary-600">0{item.number}</span>
                            </div>
                            <CardTitle>{item.title}</CardTitle>
                            <CardDescription>{item.description}</CardDescription>
                        </div>
                    </Card>
                </div>
            ))}
        </div>
    );
};

export const Card = ({ className, children }) => {
    return (
        <div
            className={cn(
                "rounded-2xl h-full w-full overflow-hidden bg-transparent border border-transparent group-hover:border-primary-200 relative z-20 transition-colors duration-500",
                className
            )}
        >
            <div className="relative z-50">
                <div className="p-2">{children}</div>
            </div>
        </div>
    );
};
export const CardTitle = ({ className, children }) => {
    return (
        <h4 className={cn("text-gray-900 font-bold tracking-wide mt-2", className)}>
            {children}
        </h4>
    );
};
export const CardDescription = ({ className, children }) => {
    return (
        <p
            className={cn(
                "mt-4 text-gray-600 tracking-wide leading-relaxed text-sm",
                className
            )}
        >
            {children}
        </p>
    );
};
