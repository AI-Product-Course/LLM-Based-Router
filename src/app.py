from src.router import router
from langchain_core.runnables import RunnableLambda

TOPIC_MAPPING = {
    1: "подача документов",
    2: "входные испытания",
    3: "учебный план и дисциплины",
    4: "стажировки",
    5: "другое",
}
router_runnable = RunnableLambda(router)


if __name__ == "__main__":
    query = input("Введите вопрос: ")
    topic_number = router_runnable.invoke(query)
    topic_string = TOPIC_MAPPING.get(topic_number, "ошибка")
    print("Тематика:", topic_string)
