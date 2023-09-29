package util

import (
	// "encoding/json"

	"fmt"
	"net/http"
	"strings"
	"sync"

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

func ExampleScrape(url string) (JSONResponse, error) {

	res, err := http.Get(url)
	if err != nil {
		return JSONResponse{}, err
	}

	defer res.Body.Close()

	if res.StatusCode != 200 {
		return JSONResponse{}, fmt.Errorf("status code error: %d %s", res.StatusCode, res.Status)
	}

	doc, err := goquery.NewDocumentFromReader(res.Body)

	if err != nil {
		return JSONResponse{}, err
	}

	var data ScrapedData
	var wg sync.WaitGroup

	wg.Add(5)
	go func() {
		defer wg.Done()
		doc.Find("h1").Each(func(i int, s *goquery.Selection) {
			text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
			data.H1 = append(data.H1, text)
		})
	}()

	go func() {
		defer wg.Done()
		doc.Find("h2").Each(func(i int, s *goquery.Selection) {
			text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
			data.H2 = append(data.H2, text)
		})
	}()

	go func() {
		defer wg.Done()
		doc.Find("h3").Each(func(i int, s *goquery.Selection) {
			text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
			data.H3 = append(data.H3, text)
		})
	}()

	go func() {
		defer wg.Done()
		doc.Find("p").Each(func(i int, s *goquery.Selection) {
			text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
			data.P = append(data.P, text)
		})
	}()
	go func() {
		defer wg.Done()
		doc.Find("a").Each(func(i int, s *goquery.Selection) {
			text := strings.Replace(strings.Replace(strings.TrimSpace(s.Text()), "\n", "", -1), "\t", "", -1)
			data.A = append(data.A, text)
		})
	}()

	wg.Wait()

	return JSONResponse(data), nil
}
