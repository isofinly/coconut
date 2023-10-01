export async function GET(request) {
  const url = new URL(request.url);
  const domain = url.searchParams.get("domain");

  if (!domain) {
    let error_response = {
      status: "fail",
      message: "No 'domain' parameter provided in the URL",
    };
    return new Response(JSON.stringify(error_response), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Assuming you have a way to fetch category and theme based on the provided domain.
  // Replace the following lines with your actual logic to retrieve category and theme.
  const category = `${domain}`; // Replace with your actual logic
  const theme = "Theme name"; // Replace with your actual logic

  let json_response = {
    category,
    theme,
  };

  return new Response(JSON.stringify(json_response), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}
