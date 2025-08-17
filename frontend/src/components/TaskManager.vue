<template>
    <div id="taskManager">
        <div v-bind:key="task.id" v-for="task in tasks">
            <TasksTitle v-bind:task = "task" v-on:del-task = "$emit('del-task', task.id)"/>
            </div>
    </div>
</template>

<script>
import TasksTitle from "./Task.vue"
export default {
    components: {
        TasksTitle
    },
    name: "TaskManager",
    props: ["tasks"]
    
}
</script>

<style>

</style>