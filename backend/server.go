package main

import (

	"log"
	"encoding/json"

	"github.com/gofiber/fiber/v2"

	"github.com/isofinly/coconut/util"
	)

func main() {
	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, World!")
	})

	app.Post("/", func(c *fiber.Ctx) error {
		type RequestBody struct {
			URL string `json:"url"`
		}

		var reqBody RequestBody
		if err := json.Unmarshal(c.Body(), &reqBody); err != nil {
			return err
		}

		result := util.ExampleScrape(reqBody.URL)

		jsonResponse, err := json.Marshal(result)
		if err != nil {
			log.Println(err)
		}

		return c.SendString(string(jsonResponse))
	})

	app.Listen(":3030")
}
