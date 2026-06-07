from dishka import Provider, Scope, provide

from application import interactors


class AppProvider(Provider):

    create_client_interactor = provide(interactors.CreateClient, scope=Scope.REQUEST)
    get_client_by_id_interactor = provide(interactors.GetClientByID, scope=Scope.REQUEST)
    get_client_by_uuid_interactor = provide(interactors.GetClientByUUID, scope=Scope.REQUEST)
    get_client_by_phone_interactor = provide(interactors.GetClientByPhone, scope=Scope.REQUEST)
    get_clients_interactor = provide(interactors.GetClients, scope=Scope.REQUEST)

    create_order_interactor = provide(interactors.CreateOrder, scope=Scope.REQUEST)
    get_order_interactor = provide(interactors.GetOrder, scope=Scope.REQUEST)
    get_orders_interactor = provide(interactors.GetOrders, scope=Scope.REQUEST)

    create_product_interactor = provide(interactors.CreateProduct, scope=Scope.REQUEST)
    get_product_interactor = provide(interactors.GetProduct, scope=Scope.REQUEST)
    get_products_interactor = provide(interactors.GetProducts, scope=Scope.REQUEST)
