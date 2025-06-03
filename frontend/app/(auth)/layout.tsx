export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    // <div className="min-h-screen bg-gray-100 flex items-center justify-center">
    //   {children}
    // </div>
    <div className="w-full">
      {" "}
      <nav className="border border-red-300">
        <h1>KnoWord</h1>
      </nav>
      <div>{children}</div>
    </div>
  );
}
