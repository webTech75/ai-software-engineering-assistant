

type LandingHeaderProps = {
  onLogin: () => void;
};

export function LandingHeader({ onLogin}: LandingHeaderProps) {

  return (
    <header className="absolute inset-x-0 top-0 z-50 flex justify-end px-6 py-6 lg:px-12">
      {/* <Logo /> */}

      <button
        onClick={onLogin}
        className="
          rounded-full
          border
          border-border
          bg-background/40
          px-6
          py-2
          text-sm
          font-medium
          backdrop-blur-md
          transition
          hover:bg-accent
        "
      >
        Login
      </button>
    </header>
  );
}