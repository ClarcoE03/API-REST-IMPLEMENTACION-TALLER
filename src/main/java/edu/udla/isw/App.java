package edu.udla.isw;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.main.Main;

public class App extends RouteBuilder {

    public static void main(String[] args) throws Exception {
        Main main = new Main();
        main.configure().addRoutesBuilder(new App());
        main.run(args);
    }

    @Override
    public void configure() {

        // Configuración REST + Swagger
        restConfiguration()
                .component("netty-http")
                .port(8080)
                .contextPath("/api")
                .apiContextPath("/api-doc")
                .apiProperty("api.title", "API de Envíos")
                .apiProperty("api.version", "1.0.0")
                .apiProperty("api.description", "API REST para registrar y consultar envíos");

        // Definición de endpoints REST
        rest("/envios").description("Gestión de Envíos")
                .get()
                    .description("Listar todos los envíos")
                    .to("direct:listarEnvios")
                .post()
                    .description("Crear un nuevo envío")
                    .to("direct:crearEnvio");

        rest("/envios/{id}")
                .get()
                    .description("Obtener un envío por ID")
                    .to("direct:obtenerEnvio");

        // Rutas internas Camel

        // GET /envios
        from("direct:listarEnvios")
                .setBody(constant(
                        "[{\"id\":\"001\",\"destinatario\":\"Juan Pérez\",\"direccion\":\"Av. Siempre Viva 123\",\"estado\":\"En tránsito\"}]"
                ));

        // POST /envios
        from("direct:crearEnvio")
                .log("Nuevo envío recibido: ${body}")
                .setHeader("Content-Type", constant("application/json"))
                .setBody(constant("{\"mensaje\":\"Envío registrado correctamente\"}"));

        // GET /envios/{id}
        from("direct:obtenerEnvio")
                .log("Consultando envío con ID: ${header.id}")
                .setHeader("Content-Type", constant("application/json"))
                .setBody(simple(
                        "{\"id\":\"${header.id}\",\"destinatario\":\"Cliente X\",\"direccion\":\"Calle Falsa 123\",\"estado\":\"Entregado\"}"
                ));
    }
}
