scalaVersion := "3.3.4"
name := "orders"

libraryDependencies ++= Seq(
  "org.apache.pekko" %% "pekko-actor-typed" % "1.1.2",
  "org.apache.pekko" %% "pekko-stream" % "1.1.2",
  "org.apache.pekko" %% "pekko-http" % "1.1.0"
)

Compile / mainClass := Some("orders.Main")
