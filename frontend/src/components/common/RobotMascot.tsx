import { useEffect, useRef, useState } from "react";

export type RobotMood = "idle" | "typing" | "password" | "error" | "loading";

type Props = {
  mood: RobotMood;
  typingProgress?: number; // 0..1, how far along the username field you are
};

const EYES = [
  { cx: 72, cy: 92 },
  { cx: 128, cy: 92 },
];
const MAX_LOOK = 7;

export function RobotMascot({ mood, typingProgress = 0.5 }: Props){
  const svgRef = useRef<SVGSVGElement>(null);
  const [look, setLook] = useState({ x: 0, y: 0 });
  const [blink, setBlink] = useState(false);

  // follow the cursor while idle
  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      const el = svgRef.current;
      if (!el) return;
      const r = el.getBoundingClientRect();
      const dx = e.clientX - (r.left + r.width / 2);
      const dy = e.clientY - (r.top + r.height / 2);
      const dist = Math.hypot(dx, dy) || 1;
      const k = Math.min(dist / 250, 1);
      setLook({ x: (dx / dist) * k, y: (dy / dist) * k });
    };
    window.addEventListener("mousemove", onMove);
    return () => window.removeEventListener("mousemove", onMove);
  }, []);

  // random blinking
  useEffect(() => {
    let timeout: number;
    const schedule = () => {
      timeout = window.setTimeout(() => {
        setBlink(true);
        window.setTimeout(() => setBlink(false), 140);
        schedule();
      }, 2500 + Math.random() * 3000);
    };
    schedule();
    return () => clearTimeout(timeout);
  }, []);

  // where the pupils point, depending on mood
  let target = look;
  if (mood === "typing") target = { x: (typingProgress - 0.5) * 1.6, y: 0.8 };
  if (mood === "error") target = { x: 0, y: 0.3 };

  const eyesClosed = mood === "password" || blink;
  const antennaColor =
    mood === "error" ? "var(--destructive)" : "var(--primary)";

  return (
    <svg
      ref={svgRef}
      viewBox="0 0 200 200"
      className={`robot mx-auto h-28 w-28 ${mood === "error" ? "robot-shake" : ""}`}
      aria-hidden="true"
    >
      <defs>
        {EYES.map((e, i) => (
          <clipPath id={`eye-clip-${i}`} key={i}>
            <circle cx={e.cx} cy={e.cy} r={20} />
          </clipPath>
        ))}
      </defs>

      {/* antenna */}
      <line x1="100" y1="30" x2="100" y2="52" stroke="var(--border)" strokeWidth="4" />
      <circle
        cx="100"
        cy="24"
        r="7"
        fill={antennaColor}
        className={mood === "loading" ? "robot-pulse-fast" : "robot-pulse"}
      />

      {/* ears */}
      <rect x="18" y="82" width="12" height="28" rx="5" fill="var(--primary)" opacity="0.7" />
      <rect x="170" y="82" width="12" height="28" rx="5" fill="var(--primary)" opacity="0.7" />

      {/* head */}
      <rect
        x="30"
        y="52"
        width="140"
        height="110"
        rx="26"
        fill="var(--card)"
        stroke="var(--primary)"
        strokeWidth="3"
      />

      {/* eyes */}
      {EYES.map((e, i) => (
        <g key={i}>
          <circle cx={e.cx} cy={e.cy} r={20} fill="var(--background)" stroke="var(--border)" strokeWidth="2" />
          <circle
            cx={e.cx + target.x * MAX_LOOK}
            cy={e.cy + target.y * MAX_LOOK}
            r={9}
            fill="var(--primary)"
            style={{ transition: "cx 0.12s ease-out, cy 0.12s ease-out" }}
          />
          <circle
            cx={e.cx + target.x * MAX_LOOK + 3}
            cy={e.cy + target.y * MAX_LOOK - 3}
            r={2.5}
            fill="var(--primary-foreground)"
            style={{ transition: "cx 0.12s ease-out, cy 0.12s ease-out" }}
          />
          {/* eyelid */}
          <g clipPath={`url(#eye-clip-${i})`}>
            <rect
              x={e.cx - 22}
              y={e.cy - 22}
              width={44}
              height={44}
              fill="var(--card)"
              style={{
                transformOrigin: `${e.cx}px ${e.cy - 22}px`,
                transform: `scaleY(${eyesClosed ? 1 : 0})`,
                transition: "transform 0.15s ease",
              }}
            />
          </g>
        </g>
      ))}

      {/* mouth */}
      {mood === "error" ? (
        <path d="M78 140 Q100 126 122 140" fill="none" stroke="var(--destructive)" strokeWidth="4" strokeLinecap="round" />
      ) : mood === "password" ? (
        <line x1="86" y1="136" x2="114" y2="136" stroke="var(--muted-foreground)" strokeWidth="4" strokeLinecap="round" />
      ) : (
        <path d="M78 130 Q100 148 122 130" fill="none" stroke="var(--primary)" strokeWidth="4" strokeLinecap="round" />
      )}
    </svg>
  );
}