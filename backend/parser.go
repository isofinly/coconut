package main

import (
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

func ExampleScrape() ScrapedData {
	// Request the HTML page.
	res, err := http.Get("http://metalsucks.net")
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}

	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Find the required elements
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
	return data
}

// func parserMain() {
// 	data := ExampleScrape()
// 	fmt.Printf("%v\n", data)
// 	// ExampleScrape()
// }
