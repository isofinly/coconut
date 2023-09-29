package main

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"

	"github.com/goccy/go-json"
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

		return c.SendString("Hello world")
	})

	app.Listen(":3030")
}
