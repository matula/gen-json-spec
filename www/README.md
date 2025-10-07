# Family Tree Viewer

This is a web-based family tree viewer for gen-json files. It allows you to visualize your family tree and view details about each individual.

## Features

- Load gen-json files to view your family tree
- View a hierarchical tree representation of your family
- Click on individuals to see their detailed information
- Navigate between related individuals (parents, spouses, children)
- Responsive design that works on desktop and mobile devices

## How to Use

1. Open `index.html` in a web browser
2. Either:
   - Click "Load Example" to view the example family tree, or
   - Use the file input to upload your own gen-json file
3. The family tree will be displayed on the left side
4. Click on any person in the tree to view their details on the right side
5. In the details panel, you can click on related individuals (parents, spouses, children) to navigate to them

## Technical Details

The viewer is built with vanilla JavaScript, HTML, and CSS. It doesn't require any external libraries or frameworks.

The family tree is rendered as a hierarchical structure, starting with individuals who don't have parents (root individuals). Each person is displayed with their name and birth/death years, and their descendants are shown beneath them with connecting lines.

The viewer supports all the fields defined in the gen-json specification, including:
- Personal information (name, sex)
- Birth and death details (date, place)
- Family relationships (parents, spouses, children)

## Browser Compatibility

This viewer works in all modern browsers, including:
- Chrome
- Firefox
- Safari
- Edge
