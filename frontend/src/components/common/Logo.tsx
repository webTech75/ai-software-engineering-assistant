import RobotLogo from "./RebotLogo";

export function Logo() {
  return (
    <div className="flex items-center gap-3">
      <RobotLogo className="h-9 w-9" />
      {/* <span className="text-2xl">🤖</span> */}

      <div>
        <h1 className="text-lg font-semibold">
          AI Software Engineering Assistant
        </h1>

        <p className="text-xs text-muted-foreground">
          Your AI Pair Programmer
        </p>
      </div>
    </div>
  );
}