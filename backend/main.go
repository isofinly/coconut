package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"

	"github.com/goccy/go-json"
	"github.com/isofinly/coconut/util"
)

func main() {
	app := fiber.New(fiber.Config{
		// Prefork:     true,
		JSONEncoder: json.Marshal,
		JSONDecoder: json.Unmarshal,
	})

	app.Use(logger.New())

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

		result, err := util.ExampleScrape(reqBody.URL)
		if err != nil {
			log.Println(err)
			return c.SendStatus(500)
		}

		jsonResponse, err := json.Marshal(result)
		if err != nil {
			log.Println(err)
		}

		return c.SendString(string(jsonResponse))
	})

	app.Listen(":3030")
}
