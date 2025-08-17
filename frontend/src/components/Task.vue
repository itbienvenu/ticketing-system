<template>
    <div class="task-item" v-bind:class="{'is-completed': task.completed}">
        <input type="checkbox" v-on:change="markComplete">
        {{task.title}}
        <button @click="$emit('del-task', task.id)">Delete Task</button>
    </div>
</template>

<script>
/* eslint-disable */
export default {
    name: "TasksTitle",
    props: ["task"], 
    methods: {
        markComplete() {
            this.task.completed = !this.task.completed
        }
    }
}
</script>

<style>
    .task-item {
        background: #f4f4f4;
        padding: 10px;
        border-bottom: 1px #ccc dotted;
    }
    .is-completed {
        text-decoration: line-through;
    }
</style>