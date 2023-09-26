"use client";
import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Divider,
  Input,
  Skeleton,
  Spacer,
} from "@nextui-org/react";
import { useState } from "react";

export default function Home() {
  const [inputUrl, setInputUrl] = useState("");
  return (
    <main className="flex min-h-screen flex-col p-24">
      <div className="grid grid-flow-row-dense grid-cols-2 gap-2 items-end">
        <Input
          className="col-span-1"
          isRequired
          type="url"
          label="Ссылка на сайт"
          placeholder=""
          labelPlacement="outside"
          value={inputUrl}
          onChange={(e) => {
            setInputUrl(e.target.value);
          }}
          startContent={
            <div className="pointer-events-none flex items-center">
              <span className="text-default-400 text-small">https://</span>
            </div>
          }
          // endContent={
          //   <div className="pointer-events-none flex items-center">
          //     <span className="text-default-400 text-small">.org</span>
          //   </div>
          // }
        />
        <Button color="primary" className="col-span-1 max-w-[50px]">
          Анализ
        </Button>
      </div>

      <Spacer x={2} />
      <div className="grid grid-flow-row-dense gap-2">
        <Card
          className="py-4 w-full col-span-2"
        >
          <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
            <p className="text-tiny uppercase font-bold">
              Анализ содержания сайта:
            </p>
            <h4 className="font-bold text-large">{inputUrl}</h4>
          </CardHeader>
          <Divider className="my-4" />
          <CardBody className="overflow-visible py-2">
            <Skeleton className="rounded-lg">
              <div className="w-full min-h-[350px]">

              </div>
            </Skeleton>
          </CardBody>
          <Divider className="my-4" />
          <CardFooter>
            <ButtonGroup>
              <Button color="primary">
                Статистика сайта
              </Button>
              <Button
                variant="flat"
                color="primary"
                onPress={() => console.log(inputUrl)}
              >
                Больше возможностей
              </Button>
            </ButtonGroup>
          </CardFooter>
        </Card>
      </div>
    </main>
  );
}
