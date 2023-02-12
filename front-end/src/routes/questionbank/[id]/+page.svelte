<script>
    export let data;
    var show_answer = false;
</script>

<div class="card m-5">
    <div class="card-body">
        {@html data.questions[0]}
        <br>
        <button on:click={() => show_answer = !show_answer} class="btn btn-primary">
            {show_answer ? "Hide" : "Show"} answer
        </button>
        {#if show_answer}
        <hr>
        {@html data.markscheme[0]}
        {/if}
    </div>
</div>