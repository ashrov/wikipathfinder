import React, { useEffect } from "react";
import lottie from "lottie-web";

export interface LottieAnimationProps {
    animationData: object;
}

export const LottieAnimation: React.FC<LottieAnimationProps> = ({
    animationData,
}) => {
    const containerRef = React.useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (containerRef.current !== null) {
            const anim = lottie.loadAnimation({
                container: containerRef.current,
                renderer: "svg",
                loop: true,
                autoplay: true,
                animationData: animationData,
            });

            return () => {
                anim.destroy();
            };
        }
    }, [animationData]);

    return <div ref={containerRef}></div>;
};
