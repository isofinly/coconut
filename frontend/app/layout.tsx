import './globals.css'


export const metadata = {
  title: "Coconut AI Assistant",
  description: "-",
};


export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  )
}
