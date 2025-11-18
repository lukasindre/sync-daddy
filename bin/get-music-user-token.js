#!/usr/bin/env node
import http from "http";
import { exec } from "child_process";
import url from "url";

const args = process.argv.slice(2);
const devTokenFlag = args.indexOf("--dev-token");
if (devTokenFlag === -1 || !args[devTokenFlag + 1]) {
  console.error("Usage: node get-music-user-token.js --dev-token <token>");
  process.exit(1);
}
const developerToken = args[devTokenFlag + 1];

// Start local server to receive MUT
const PORT = 3123;

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url, true);

  if (parsed.pathname === "/") {
    // Serve browser page
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(buildHtml(developerToken));
    return;
  }

  if (parsed.pathname === "/token") {
    const { userToken } = parsed.query;

    if (!userToken) {
      res.writeHead(400);
      res.end("Missing token");
      return;
    }

    console.log("\n🎉 Music User Token:");
    console.log(userToken + "\n");

    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end("Token received! You can close this tab.");

    server.close();
    process.exit(0);
  }
});

// Start server and open browser
server.listen(PORT, () => {
  const url = `http://localhost:${PORT}`;
  console.log(`Opening browser for Apple Music auth…`);
  openBrowser(url);
});

function openBrowser(url) {
  const cmd =
    process.platform === "win32"
      ? `start ${url}`
      : process.platform === "darwin"
      ? `open ${url}`
      : `xdg-open ${url}`;

  exec(cmd);
}

function buildHtml(devToken) {
  return `
<!DOCTYPE html>
<html>
  <body style="font-family: sans-serif;">
    <h1>Generate Apple Music User Token</h1>
    <button id="btn">Sign In with Apple Music</button>

    <script src="https://js-cdn.music.apple.com/musickit/v3/musickit.js"></script>
    <script>
      document.getElementById("btn").onclick = async () => {
        const music = await MusicKit.configure({
          developerToken: "${devToken}",
          app: { name: "CLI Tool", build: "1.0" },
        });

        const userToken = await music.authorize();

        // Send back to CLI
        fetch("/token?userToken=" + encodeURIComponent(userToken));
      };
    </script>
  </body>
</html>`;
}
