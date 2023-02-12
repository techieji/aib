export async function load({ fetch, params }) {
    let resp = await fetch(`http://127.0.0.1:8080/api/question/${params.id}`);
    return resp.json();
}