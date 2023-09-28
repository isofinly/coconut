package util

import (
	// "encoding/json"

	"log"
	"net/http"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

type ScrapedData struct {
	H1 []string
	H2 []string
	H3 []string
	A  []string
	P  []string
}

type JSONResponse struct {
	H1 []string `json:"h1"`
	H2 []string `json:"h2"`
	H3 []string `json:"h3"`
	A  []string `json:"a"`
	P  []string `json:"p"`
}

// TODO: 
// Proper error handling to prevent server from exit(1);
// rewrite doc.Find to one doc.Find("h1", "h2", "h3", "a", "p") with proper field identification

// <meta> parse ???

func ExampleScrape(url string) JSONResponse  {

	res, err := http.Get(url)

	if err != nil {
		log.Fatal(err)
	}

	defer res.Body.Close()

	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}

	doc, err := goquery.NewDocumentFromReader(res.Body)

	if err != nil {
		log.Fatal(err)
	}
	
	var data ScrapedData
	doc.Find("h1").Each(func(i int, s *goquery.Selection) {
		text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
		data.H1 = append(data.H1, text)
	})
	doc.Find("h2").Each(func(i int, s *goquery.Selection) {
		text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
		data.H2 = append(data.H2, text)
	})
	doc.Find("h3").Each(func(i int, s *goquery.Selection) {
		text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
		data.H2 = append(data.H3, text)
	})
	doc.Find("p").Each(func(i int, s *goquery.Selection) {
		text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
		data.P = append(data.P, text)
	})
	doc.Find("a").Each(func(i int, s *goquery.Selection) {
		text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
		data.A = append(data.A, text)
	})

	jsonData := JSONResponse{
		H1: data.H1,
		H2: data.H2,
		H3: data.H3,
		A:  data.A,
		P:  data.P,
	}

	return jsonData
}

