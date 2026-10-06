package orders

import org.apache.pekko.actor.typed.ActorSystem
import org.apache.pekko.actor.typed.scaladsl.Behaviors
import org.apache.pekko.http.scaladsl.Http
import org.apache.pekko.http.scaladsl.model.{ContentTypes, HttpEntity, StatusCodes}
import org.apache.pekko.http.scaladsl.server.Directives.*

object Main:
  private def json(s: String) = HttpEntity(ContentTypes.`application/json`, s)

  def main(args: Array[String]): Unit =
    given system: ActorSystem[Nothing] = ActorSystem(Behaviors.empty, "orders")
    val port = sys.env.get("PORT").map(_.toInt).getOrElse(8080)
    val routes =
      concat(
        path("health")(get(complete(json("""{"status":"UP"}""")))),
        path("orders" / Segment) { raw =>
          get {
            raw.toLongOption.filter(_ >= 0) match
              case Some(id) =>
                complete(json(s"""{"id":$id,"customer":"c-${id % 100}","total":${id % 1000}.5,"status":"NEW"}"""))
              case None => complete(StatusCodes.BadRequest, json("""{"error":"bad id"}"""))
          }
        }
      )
    Http().newServerAt("0.0.0.0", port).bind(routes)
