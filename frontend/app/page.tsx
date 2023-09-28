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
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Skeleton,
  Spacer,
  Tab,
  Tabs,
  useDisclosure,
} from "@nextui-org/react";
import axios from "axios";
import React, { Key } from "react";
import { useState } from "react";

export default function Home() {
  const {
    isOpen: isCardOpen,
    onOpen: onCardOpen,
    onClose: onCardClose,
  } = useDisclosure();

  const [selected, setSelected] = useState<Key | null>(null);
  const [inputUrl, setInputUrl] = useState("");
  const [data, setData] = useState(null); // Specify the type explicitly
  const [error, setError] = useState<Error | null>(null); // Specify the type explicitly

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:3030/", {
        url: "https://" + inputUrl,
      });
      setData(response.data);
      setError(null);
    } catch (error) {
      setError(error as Error);
      setData(null);
    }
  };

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
        <Button
          color="primary"
          className="col-span-1 max-w-[50px]"
          onPress={() => handleSubmit()}
        >
          Анализ
        </Button>
      </div>

      <Spacer x={2} />
      <div className="grid grid-flow-row-dense gap-2">
        <Card className="py-4 w-full col-span-2">
          <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
            <p className="text-tiny uppercase font-bold">
              Анализ содержания сайта:
            </p>
            <h4 className="font-bold text-large">{inputUrl}</h4>
          </CardHeader>
          <Divider className="my-4" />
          <CardBody className="overflow-visible py-2">
            <Skeleton className="rounded-lg">
              <div className="w-full min-h-[350px]"></div>
            </Skeleton>
          </CardBody>
          <Divider className="my-4" />
          <CardFooter>
            <ButtonGroup>
              <Button color="primary" onPress={() => handleSubmit()}>
                Краткое содержание
              </Button>
              <Button
                variant="flat"
                color="primary"
                onPress={() => onCardOpen()}
              >
                Больше возможностей
              </Button>
            </ButtonGroup>
          </CardFooter>
        </Card>
        <Modal
          isDismissable={false}
          size="5xl"
          isOpen={isCardOpen}
          onClose={onCardClose}
          backdrop="blur"
        >
          <ModalContent>
            {(onClose) => (
              <>
                <ModalHeader className="flex flex-col gap-1">Cards</ModalHeader>
                <ModalBody>
                  <Tabs
                    fullWidth
                    size="md"
                    aria-label="Tabs div"
                    selectedKey={selected}
                    onSelectionChange={setSelected}
                  >
                    <Tab key="new-user" title="User register">
                      <div className="flex flex-col gap-4">
                        <Input
                          isRequired
                          label="Email"
                          placeholder="Enter your email"
                          type="email"
                        />
                        <Input
                          isRequired
                          label="Password"
                          placeholder="Enter your password"
                          type="password"
                        />

                        <div className="flex gap-2 justify-end">
                          <Button fullWidth color="primary">
                            Login
                          </Button>
                        </div>
                      </div>
                    </Tab>
                    <Tab key="state-change" title="State change">
                      <div className="flex flex-col gap-4 h-[300px]">
                        <Input
                          isRequired
                          label="Name"
                          placeholder="Enter your name"
                          type="password"
                        />
                        <Input
                          isRequired
                          label="Email"
                          placeholder="Enter your email"
                          type="email"
                        />
                        <Input
                          isRequired
                          label="Password"
                          placeholder="Enter your password"
                          type="password"
                        />

                        <div className="flex gap-2 justify-end">
                          <Button fullWidth color="primary">
                            Sign up
                          </Button>
                        </div>
                      </div>
                    </Tab>
                  </Tabs>
                </ModalBody>
                <ModalFooter>
                  <ButtonGroup>
                    <Button color="danger" variant="flat" onPress={onClose}>
                      Close
                    </Button>
                    <Button
                      color="default"
                      variant="bordered"
                      onPress={onClose}
                    >
                      Справка
                    </Button>
                  </ButtonGroup>
                </ModalFooter>
              </>
            )}
          </ModalContent>
        </Modal>
      </div>
    </main>
  );
}
