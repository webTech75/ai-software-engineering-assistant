type Props = { className?: string };

export default function RobotLogo({ className = "h-9 w-9" }: Props) {
  return (
    <svg viewBox="0 0 200 200" className={className} aria-hidden="true">
      <line x1="100" y1="30" x2="100" y2="52" stroke="var(--border)" strokeWidth="6" />
      <circle cx="100" cy="24" r="10" fill="var(--primary)" />

      <rect x="14" y="82" width="16" height="32" rx="6" fill="var(--primary)" opacity="0.7" />
      <rect x="170" y="82" width="16" height="32" rx="6" fill="var(--primary)" opacity="0.7" />

      <rect x="30" y="52" width="140" height="110" rx="26" fill="var(--card)" stroke="var(--primary)" strokeWidth="6" />

      <circle cx="72" cy="94" r="20" fill="var(--background)" stroke="var(--border)" strokeWidth="3" />
      <circle cx="128" cy="94" r="20" fill="var(--background)" stroke="var(--border)" strokeWidth="3" />
      <circle cx="74" cy="96" r="9" fill="var(--primary)" />
      <circle cx="130" cy="96" r="9" fill="var(--primary)" />

      <path d="M78 132 Q100 150 122 132" fill="none" stroke="var(--primary)" strokeWidth="6" strokeLinecap="round" />
    </svg>
  );
}