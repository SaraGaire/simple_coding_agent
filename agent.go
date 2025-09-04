package main

import (
    "fmt"
    "io/ioutil"
    "os"
    "os/exec"
    "strings"
)

type CodingAgent struct {
    APIKey string
}

func NewCodingAgent(apiKey string) *CodingAgent {
    return &CodingAgent{APIKey: apiKey}
}

func (ca *CodingAgent) GenerateCode(prompt, language string) string {
    templates := map[string]string{
        "function": `func %s(%s) %s {
    // %s
    // TODO: Implement function logic
}`,
        "struct": `type %s struct {
    // %s
    // TODO: Add struct fields
}`,
        "main": `package main

import "fmt"

// %s
func main() {
    // TODO: Implement main logic
    fmt.Println("Hello, World!")
}`,
    }

    prompt = strings.ToLower(prompt)
    if strings.Contains(prompt, "function") {
        return fmt.Sprintf(templates["function"], 
            "newFunction", "", "", "Generated function")
    } else if strings.Contains(prompt, "struct") {
        return fmt.Sprintf(templates["struct"], 
            "NewStruct", "Generated struct")
    } else {
        return fmt.Sprintf(templates["main"], "Generated program")
    }
}

func (ca *CodingAgent) SaveCode(code, filename string) error {
    return ioutil.WriteFile(filename, []byte(code), 0644)
}

func (ca *CodingAgent) ExecuteCode(filename string) (string, error) {
    cmd := exec.Command("go", "run", filename)
    output, err := cmd.CombinedOutput()
    return string(output), err
}

func (ca *CodingAgent) AnalyzeCode(filename string) (map[string]int, error) {
    content, err := ioutil.ReadFile(filename)
    if err != nil {
        return nil, err
    }
    
    code := string(content)
    analysis := map[string]int{
        "lines":     len(strings.Split(code, "\n")),
        "functions": strings.Count(code, "func "),
        "structs":   strings.Count(code, "type "),
        "imports":   strings.Count(code, "import"),
    }
    
    return analysis, nil
}

func main() {
    agent := NewCodingAgent("")
    code := agent.GenerateCode("Create a main function", "go")
    
    err := agent.SaveCode(code, "example.go")
    if err != nil {
        fmt.Printf("Error saving code: %v\n", err)
        return
    }
    
    output, err := agent.ExecuteCode("example.go")
    if err != nil {
        fmt.Printf("Error executing code: %v\n", err)
    }
    fmt.Printf("Output: %s\n", output)
    
    // Clean up
    os.Remove("example.go")
}
