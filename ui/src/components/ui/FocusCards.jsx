import React, { useState } from "react";
import { cn } from "@utils/helpers";

export const Card = ({
    card,
    index,
    hovered,
    setHovered,
}) => {
    return (
        <div
            onMouseEnter={() => setHovered(index)}
            onMouseLeave={() => setHovered(null)}
            className={cn(
                "rounded-xl relative bg-white overflow-hidden h-full transition-all duration-300 ease-out border border-neutral-200 shadow-sm",
                hovered !== null && hovered !== index && "blur-sm scale-[0.98] opacity-50",
                hovered === index && "scale-[1.02] shadow-xl ring-2 ring-primary-500/20 z-10"
            )}
        >
            <div className="p-6 h-full flex flex-col">
                <div className="bg-primary-50 w-12 h-12 rounded-lg flex items-center justify-center mb-4 text-primary-600">
                    {card.icon}
                </div>
                <div className="font-semibold text-xl text-neutral-900 mb-2">
                    {card.title}
                </div>
                <div className="text-neutral-600">
                    {card.description}
                </div>
            </div>
        </div>
    );
};

export const FocusCards = ({ cards }) => {
    const [hovered, setHovered] = useState(null);

    return (
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto w-full">
            {cards.map((card, index) => (
                <Card
                    key={card.title}
                    card={card}
                    index={index}
                    hovered={hovered}
                    setHovered={setHovered}
                />
            ))}
        </div>
    );
};

export default FocusCards;
