package dev.anurag.RAG.System.controller;


import dev.anurag.RAG.System.response.RagResponse;
import dev.anurag.RAG.System.service.RagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/query")
public class RagController {

    @Autowired
    private RagService ragService;

    @PostMapping
    public ResponseEntity<?> query(@RequestBody Map<String, String> request) {
        try {
            String question = request.get("query");
            RagResponse response = ragService.getAnswer(question);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
}
