package dev.anurag.RAG.System.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import dev.anurag.RAG.System.response.RagResponse;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class RagService {

    public RagResponse getAnswer(String question) throws Exception {
        String url = "http://localhost:5000/rag/query";

        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, String> payload = Map.of("query", question);

        HttpEntity<Map<String, String>> entity = new HttpEntity<>(payload, headers);
        ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);

        ObjectMapper mapper = new ObjectMapper();
        JsonNode root = mapper.readTree(response.getBody());

        if (root.has("error")) {
            String errorMsg = root.get("error").asText();
            String details = root.has("details") ? root.get("details").asText() : "";
            throw new RuntimeException(errorMsg + " - " + details);
        }

        return mapper.treeToValue(root, RagResponse.class);
    }
}
