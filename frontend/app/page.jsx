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
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Pagination,
  getKeyValue,
} from "@nextui-org/react";

import PublishIcon from "@mui/icons-material/Publish";
import GetAppIcon from "@mui/icons-material/GetApp";
import axios from "axios";
import React, { Key } from "react";
import { useState } from "react";

export default function Home() {
  const {
    isOpen: isCardOpen,
    onOpen: onCardOpen,
    onClose: onCardClose,
  } = useDisclosure();

  const [selected, setSelected] = useState(0);
  const [inputUrl, setInputUrl] = useState("");
  const [data, setData] = useState(null); // Specify the type explicitly
  const array1 = [];

  const handleSubmit = async () => {
    try {
      const response = await axios.get("http://localhost:5000/", {
        url: "https://" + getDomainName(inputUrl),
      });
      // setData(response.data);
      if (response){
        setData(response.data)
      }
      array1.push(data)
    } catch (error) {
      setData(null);
    }
  };

  function getDomainName(url) {
    let domain = url.replace(/^(https?:\/\/)?(www\.)?/i, "");
    domain = domain.split("/")[0];
    return domain;
  }

  const [interestPage, setInterestPage] = React.useState(1); // Changed 'page' to 'interestPage'
  const rowsPerPage = 15;
  const [interest, setInterest] = React.useState([]); // Changed 'users' to 'interest'


  async function fetchInterest() {
    try {
      const response = await axios.post("http://localhost:3030/get_interest_over_time", {
        query: array1
      });
      if (response) {
        const data = await response.data
        setInterest(data?.interest_over_time);
      } else {
        // Handle error if the API request fails
      }
    } catch (error) {
      // Handle network or other errors
    }
  }

  const interest_pages = Math.ceil(interest.length / rowsPerPage);

  const interest_items = React.useMemo(() => {
    const start = (interestPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    return interest.slice(start, end);
  }, [interestPage, interest]);

  const [relatedQueriesPage, setRelatedQueriesPage] = React.useState(1);
  const queriesPerPage = 15;
  const [relatedQueries, setRelatedQueries] = React.useState([]);

  async function fetchRelatedQueries() {
    try {
      const response = await axios.post("http://localhost:3030/get_related_queries", {
        query: array1
      });
      if (response) {
        const data = await response.data
        setRelatedQueries(data?.related_queries);
      } else {
        // Handle error if the API request fails
      }
    } catch (error) {
      // Handle network or other errors
    }
  }

  const relatedQueriesPages = Math.ceil(relatedQueries.length / queriesPerPage);

  const relatedQueriesItems = React.useMemo(() => {
    const start = (relatedQueriesPage - 1) * queriesPerPage;
    const end = start + queriesPerPage;

    return relatedQueries.slice(start, end);
  }, [relatedQueriesPage, relatedQueries]);

  const [topicsPage, setTopicsPage] = React.useState(1);
  const topicsPerPage = 15;
  const [relatedTopics, setRelatedTopics] = React.useState([]);

  async function fetchRelatedTopics() {
    try {
      const response = await axios.post("http://localhost:3030/get_related_topics", {
        query: array1
      });
      if (response) {
        const data = await response.data
        setRelatedTopics(data?.related_topics);
      } else {
        // Handle error if the API request fails
      }
    } catch (error) {
      // Handle network or other errors
    }
  }

  const relatedTopicsPages = Math.ceil(relatedTopics.length / topicsPerPage);

  const relatedTopicsItems = React.useMemo(() => {
    const start = (topicsPage - 1) * topicsPerPage;
    const end = start + topicsPerPage;

    return relatedTopics.slice(start, end);
  }, [topicsPage, relatedTopics]);

  function fetchData() {
    onCardOpen();
    fetchRelatedTopics();
    fetchRelatedQueries();
    fetchInterest();
  }

  function combineJSONsAndDownload(filename, ...jsons) {
    const combined = jsons.map((json, index) => ({ [index]: json }));
    const combinedJSON = [combined];
  
    const jsonBlob = new Blob([JSON.stringify(combinedJSON)], { type: 'application/json' });
    const url = URL.createObjectURL(jsonBlob);
  
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
  
    document.body.appendChild(a);
    a.click();
  
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

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
              <Button
                color="primary"
                onPress={() => (inputUrl && (window.location.href = `https://${inputUrl}`))}
              >
                Перейти
              </Button>
              <Button
                variant="flat"
                color="primary"
                onPress={() => fetchData()}
              >
                Детальная информация
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
                <ModalHeader className="flex flex-col gap-1">
                  Информация Google Trends
                </ModalHeader>
                <ModalBody>
                  <Tabs
                    fullWidth
                    size="md"
                    aria-label="Tabs div"
                    selectedKey={selected}
                    onSelectionChange={setSelected}
                  >
                    <Tab key="interest" title="Интерес по времени">
                      <div className="flex flex-col gap-4">
                        <Table
                          aria-label="Example table with client side pagination"
                          bottomContent={
                            <div className="flex w-full justify-center">
                              <Pagination
                                isCompact
                                showControls
                                showShadow
                                color="primary"
                                page={interestPage}
                                total={interest_pages}
                                onChange={(page) => setInterestPage(page)}
                              />
                            </div>
                          }
                          classNames={{
                            wrapper: "min-h-[222px]",
                          }}
                        >
                          <TableHeader>
                            <TableColumn key="timestamp">Время</TableColumn>
                            <TableColumn key="interest">Интерес</TableColumn>
                          </TableHeader>
                          <TableBody items={interest_items}>
                            {(item) => (
                              <TableRow key={item.id}>
                                {(columnKey) => (
                                  <TableCell>
                                    {getKeyValue(item, columnKey)}
                                  </TableCell>
                                )}
                              </TableRow>
                            )}
                          </TableBody>
                        </Table>
                      </div>
                    </Tab>
                    <Tab key="queries" title="Схожие запросы">
                      <div className="flex flex-col gap-4">
                        <Table
                          aria-label="Example table with client side pagination"
                          bottomContent={
                            <div className="flex w-full justify-center">
                              <Pagination
                                isCompact
                                showControls
                                showShadow
                                color="primary"
                                page={relatedQueriesPage}
                                total={relatedQueriesPages}
                                onChange={(page) => setRelatedQueriesPage(page)}
                              />
                            </div>
                          }
                          classNames={{
                            wrapper: "min-h-[222px]",
                          }}
                        >
                          <TableHeader>
                            <TableColumn key="query">Запрос</TableColumn>
                            <TableColumn key="interest">Интерес</TableColumn>
                          </TableHeader>
                          <TableBody items={relatedQueriesItems}>
                            {(item) => (
                              <TableRow key={item.id}>
                                {(columnKey) => (
                                  <TableCell>
                                    {getKeyValue(item, columnKey)}
                                  </TableCell>
                                )}
                              </TableRow>
                            )}
                          </TableBody>
                        </Table>
                      </div>
                    </Tab>
                    <Tab key="topics" title="Схожие темы">
                      <div className="flex flex-col gap-4">
                        <Table
                          aria-label="Example table with client side pagination"
                          bottomContent={
                            <div className="flex w-full justify-center">
                              <Pagination
                                isCompact
                                showControls
                                showShadow
                                color="primary"
                                page={topicsPage}
                                total={relatedTopicsPages}
                                onChange={(page) => setTopicsPage(page)}
                              />
                            </div>
                          }
                          classNames={{
                            wrapper: "min-h-[222px]",
                          }}
                        >
                          <TableHeader>
                            <TableColumn key="title">Запрос</TableColumn>
                            <TableColumn key="type">Категория</TableColumn>
                            <TableColumn key="interest">Интерес</TableColumn>
                          </TableHeader>
                          <TableBody items={relatedTopicsItems}>
                            {(item) => (
                              <TableRow key={item.id}>
                                {(columnKey) => (
                                  <TableCell>
                                    {getKeyValue(item, columnKey)}
                                  </TableCell>
                                )}
                              </TableRow>
                            )}
                          </TableBody>
                        </Table>
                      </div>
                    </Tab>
                  </Tabs>
                </ModalBody>
                <ModalFooter>
                  <ButtonGroup>
                    <Button color="danger" variant="flat" onPress={onClose}>
                      Закрыть
                    </Button>
                    <Button
                      color="primary"
                      endContent={<GetAppIcon />}
                      onPress={ () => (combineJSONsAndDownload('combined.json',
                        interest,
                        relatedQueries,
                        relatedTopics
                      ))}
                    >
                      Экспорт
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
