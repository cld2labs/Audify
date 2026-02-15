import React, { useEffect, useRef, useState } from "react";
import { motion, useAnimation } from "framer-motion";
import clsx from "clsx";

const RippleBackground = ({
    className,
    cellClassName,
    rows = 50,
    cols = 50,
    cellSize = 50,
    ...props
}) => {
    const [activeCell, setActiveCell] = useState(null);

    // Generate grid matrix
    const matrix = Array.from({ length: rows }).map((_, r) =>
        Array.from({ length: cols }).map((_, c) => ({
            row: r,
            col: c,
        }))
    );

    return (
        <div
            className={clsx(
                "relative flex flex-row h-full w-full overflow-hidden bg-neutral-50 z-0",
                className
            )}
            {...props}
        >
            <div className="absolute inset-0 flex flex-col items-center justify-center p-4">
                {/* Main content z-index wrapper handled by parent */}
            </div>

            <div className="absolute z-0 h-full w-full overflow-hidden flex flex-col">
                {matrix.map((row, rowIdx) => (
                    <div key={`row-${rowIdx}`} className="flex flex-row justify-center relative">
                        {row.map((cell, colIdx) => (
                            <Cell
                                key={`cell-${rowIdx}-${colIdx}`}
                                rowIdx={rowIdx}
                                colIdx={colIdx}
                                isActive={
                                    activeCell?.row === rowIdx && activeCell?.col === colIdx
                                }
                                setActiveCell={setActiveCell}
                                cellClassName={cellClassName}
                            />
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

const Cell = React.memo(({ rowIdx, colIdx, isActive, setActiveCell, cellClassName }) => {
    const controls = useAnimation();

    useEffect(() => {
        if (isActive) {
            controls.start({
                opacity: 1,
                transition: { duration: 0.5, ease: "easeOut" },
            }).then(() => {
                controls.start({
                    opacity: 0.1, // fade back to baseline
                    transition: { duration: 1 },
                });
            });
        }
    }, [isActive, controls]);

    const handleClick = () => {
        setActiveCell({ row: rowIdx, col: colIdx });
    };

    return (
        <div
            onClick={handleClick}
            onMouseEnter={() => setActiveCell({ row: rowIdx, col: colIdx })}
            className={clsx(
                "bg-transparent border-[0.5px] border-neutral-200/50 box-border select-none relative transition-colors duration-300",
                cellClassName
            )}
            style={{
                width: "3rem", // ~48px
                height: "3rem",
            }}
        >
            <motion.div
                initial={{ opacity: 0 }}
                animate={controls}
                className="absolute inset-0 bg-primary-200/40"
            />
        </div>
    );
});

Cell.displayName = "Cell";

export default RippleBackground;
