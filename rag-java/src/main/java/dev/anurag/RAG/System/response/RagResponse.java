package dev.anurag.RAG.System.response;

import java.util.List;

public class RagResponse {
    private String answer;
    private List<Citation> citations;

    public static class Citation {
        private String text;
        private String source;

        public String getText() { return text; }
        public void setText(String text) { this.text = text; }
        public String getSource() { return source; }
        public void setSource(String source) { this.source = source; }
    }

    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }
    public List<Citation> getCitations() { return citations; }
    public void setCitations(List<Citation> citations) { this.citations = citations; }
}
