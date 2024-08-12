from locust import HttpUser, task


class QuickstartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            data={"username": "admin", "password": "admin"},
        ).json()
        self.client.headers = {'Authorization': f"Bearer {response.get('access', None)}"}
    
    @task
    def get_todo_list(self):
        self.client.get("/api/v1/todo/")
        
    @task
    def get_single_todo(self):
        self.client.get("/api/v1/todo/2")

