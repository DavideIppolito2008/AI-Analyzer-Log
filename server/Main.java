package server;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) throws Exception {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        // Serve la dashboard (file statici)
        server.createContext("/", new StaticFileHandler("server/web/"));

        // Serve il risultato dell'analisi
        server.createContext("/api/results", new ResultsHandler("analysis_result.json"));

        server.setExecutor(null);
        server.start();
        System.out.println("🚀 Server started at http://localhost:" + port);
    }

    // Serve file statici
    static class StaticFileHandler implements HttpHandler {
        private final String baseDir;

        public StaticFileHandler(String baseDir) {
            this.baseDir = baseDir;
        }

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
            if (path.equals("/")) path = "/index.html";
            File file = new File(baseDir + path);

            if (file.exists() && !file.isDirectory()) {
                byte[] bytes = Files.readAllBytes(file.toPath());
                exchange.getResponseHeaders().add("Content-Type", getMimeType(path));
                exchange.sendResponseHeaders(200, bytes.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(bytes);
                }
            } else {
                exchange.sendResponseHeaders(404, -1);
            }
        }

        private String getMimeType(String path) {
            if (path.endsWith(".html")) return "text/html";
            if (path.endsWith(".js")) return "application/javascript";
            if (path.endsWith(".css")) return "text/css";
            if (path.endsWith(".json")) return "application/json";
            return "text/plain";
        }
    }

    // API che restituisce il JSON
    static class ResultsHandler implements HttpHandler {
        private final String jsonPath;

        public ResultsHandler(String jsonPath) {
            this.jsonPath = jsonPath;
        }

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");

            File jsonFile = new File(jsonPath);
            if (jsonFile.exists()) {
                byte[] jsonData = Files.readAllBytes(Paths.get(jsonPath));
                exchange.getResponseHeaders().add("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, jsonData.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(jsonData);
                }
            } else {
                String errorMsg = "{\"error\": \"File 'analysis_result.json' non trovato\"}";
                exchange.sendResponseHeaders(404, errorMsg.length());
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(errorMsg.getBytes());
                }
            }
        }
    }
}
