<template>
<div id="app">
    <HeaderLayout />
    <TaskManager v-bind:tasks="tasks" v-on:del-task = "deleteTask" />
</div>
</template>
<script>
import HeaderLayout from "./components/layouts/Header.vue"
import TaskManager from "./components/TaskManager"
export default {
    name: "app",
    components: {
        TaskManager,
        HeaderLayout
    },
    data() {
        return {
            tasks: [
                {
                    id: 1,
                    title: "Task 1",
                    completed: false
                },
                {
                    id: 2,
                    title: "Task 2",
                    completed: false
                },
                {
                    id: 3,
                    title: "Task 3",
                    completed: false
                },
            ]
        }

    },
    methods: {
        deleteTask(id) {
            this.tasks = this.tasks.filter(task => task.id !== id)
        }
    }
}
</script>
<style></style>