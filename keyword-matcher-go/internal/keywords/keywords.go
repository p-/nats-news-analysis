package keywords

import (
	"bufio"
	"fmt"
	"github.com/heussd/nats-news-keyword-matcher.go/internal/config"
	"os"
	"regexp"
	"strings"
)

type KeywordEntry struct {
	regexp regexp.Regexp
	text   string
}

var keywords []KeywordEntry

func init() {
	readFile, err := os.Open(config.KeywordsFile)
	if err != nil {
		panic(err)
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	for fileScanner.Scan() {
		var text = fileScanner.Text()

		if text == "" ||
			strings.HasPrefix(text, "#") {
			continue
		}

		fmt.Printf("Parsing \"%s\" as regex\n", text)

		var regex = regexp.MustCompile(text)
		keywords = append(keywords, KeywordEntry{
			regexp: *regex,
			text:   text,
		})
	}

	if len(keywords) == 0 {
		fmt.Println("Error: No keywords found")
		os.Exit(1)
	}
}

func Match(s string) (bool, string) {
	for _, v := range keywords {

		if v.regexp.MatchString(s) {
			return true, v.regexp.FindString(s)
		}
	}
	return false, ""
}
