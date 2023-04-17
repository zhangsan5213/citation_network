// get nodes and edges
const edges = $.parseJSON(
  $.ajax({
    url: '../static/data/edges1.json',
    dataType: 'json',
    async: false,
  }).responseText,
)

const nodes = $.parseJSON(
  $.ajax({
    url: '../static/data/nodes1.json',
    dataType: 'json',
    async: false,
  }).responseText,
)
console.log(edges)
console.log(nodes)

// 处理 nodes
const newNodes = nodes.map((node) => ({
  doi: node.id,
  id: node.index,
  title: node.title,
  date: node.pub_date,
  link: node.doi,
}))
console.log(newNodes)

// 处理 edges
const newEdges = edges.map((edge) => ({
  from: edge.from,
  to: edge.to,
  dashes: edge.type == 'dashed',
  color: colorInterpret(edge.color),
}))
console.log(newEdges)

function colorInterpret(color) {
  if (color == 'k') {
    return 'black'
  } else if (color == 'r') {
    return 'red'
  } else if (color == 'g') {
    return 'green'
  } else if (color == 'b') {
    return 'red'
  }
}

let container = document.getElementById('mydataviz')
let data = {
  nodes: newNodes,
  edges: newEdges
}
let options = {
  autoResize:true,
  // nodes: {    fixed: true  },
  interaction:{
    dragNodes: false
  },
  physics: {
    enabled: true,
    hierarchicalRepulsion: {
      nodeDistance: 700
    },
    // enabled: true,
    // hierarchicalRepulsion: {
    //   nodeDistance: 400,
    //   springLength: 10,
    // },
    // stabilization: {
    //   iterations: 500
    // },
  }
};
var network = new vis.Network(container, data, options);
network.on('click', networkOnClick)

function networkOnClick(params) {
  let index;
  console.log(params)
  if (params.nodes.length > 0) {
    index = params.nodes[0]
    newNodes.map(node => {
      if (node.id==index) {
        console.log("navigate")
        if (confirm("We will navigate to the page of the article")) {
          window.location.href = node.link
        }
      }
    })
  }
  
  // window.location.href
}