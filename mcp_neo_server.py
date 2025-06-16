# from fastmcp import MCPServer, mcp_method
from fastmcp import FastMCP
from neo4j import GraphDatabase

# Configure Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "cool@1983"  # ← Replace this with your real password

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
mcp = FastMCP("Fast MCP Neo4j server")

   
@mcp.tool()
def get_all_datasets_and_files() -> list:
    """Retrieve all datasets and their associated files from neo4j."""
    with driver.session() as session:
        result = session.run("""
            MATCH (ds:Dataset)-[:CONTAINS]->(df:DataFile)
            RETURN ds.name AS dataset, df.name AS file, df.type AS type
        """)
        return [record.data() for record in result]


@mcp.tool()
def get_features_for_file(file_name: str) -> list:
    """Retrieve all features for a given file (train_FD001 , test_FD001, rul_001) from neo4j."""
    with driver.session() as session:
        result = session.run("""
            MATCH (df:DataFile {name: $file_name})-[:HAS_FEATURE]->(f:Feature)
            OPTIONAL MATCH (f)-[:BELONGS_TO]->(c:Category)
            OPTIONAL MATCH (f)-[:MEASURED_IN]->(u:Unit)
            RETURN f.name AS feature, c.name AS category, u.name AS unit, u.description AS unit_description
        """, file_name=file_name)
        return [record.data() for record in result]


@mcp.tool()
def get_files_by_type(file_type: str) -> list:
    """Retrieve all files of a specific type from neo4j . Requires input of 'train', 'test', or 'rul'."""
    if file_type not in ["train", "test", "rul"]:
        print("Invalid file type. Must be one of: 'train', 'test', 'rul'.")
        return
    
    with driver.session() as session:
        result = session.run("""
            MATCH (df:DataFile) 
            WHERE df.type = $file_type
            RETURN df.name AS file
        """, file_type=file_type)
        return [record["file"] for record in result]


@mcp.tool()
def get_all_units() -> list:
    """Retrieve all units from the Neo4j database."""
    with driver.session() as session:
        result = session.run("""
            MATCH (u:Unit)
            RETURN u.name AS unit, u.description AS description
        """)
        return [record.data() for record in result]

# MCP Server entry point
if __name__ == "__main__":       
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)  # Runs on http://localhost:8000/mcp


# from fastmcp.server import MCPServer, mcp_method
# from neo4j import GraphDatabase
# # from fastmcp import server as mcp_server
# from fastmcp.server.server import MCPServer

# # === Neo4j Setup ===
# NEO4J_URI = "bolt://localhost:7687"
# NEO4J_USER = "neo4j"
# NEO4J_PASSWORD = "cool@1983"

# driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# # === Define Tool ===
# class Neo4jTool:
#     @mcp_method()
#     def query(self, query: str):
#         """Executes Cypher query and returns results."""
#         with driver.session() as session:
#             result = session.run(query)
#             return [record.data() for record in result]

# # === Start Server ===
# if __name__ == "__main__":
#     server = MCPServer()
        
#     server.add_tool("neo4j", Neo4jTool())
#     server.run()
