import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/mcp-workshop/blog',
    component: ComponentCreator('/mcp-workshop/blog', '5b9'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/archive',
    component: ComponentCreator('/mcp-workshop/blog/archive', '2e8'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/authors',
    component: ComponentCreator('/mcp-workshop/blog/authors', '8e3'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/mcp-workshop/blog/authors/all-sebastien-lorber-articles', '5b6'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/authors/yangshun',
    component: ComponentCreator('/mcp-workshop/blog/authors/yangshun', 'b83'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/first-blog-post',
    component: ComponentCreator('/mcp-workshop/blog/first-blog-post', '0c4'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/long-blog-post',
    component: ComponentCreator('/mcp-workshop/blog/long-blog-post', '034'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/mdx-blog-post',
    component: ComponentCreator('/mcp-workshop/blog/mdx-blog-post', '3ef'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/tags',
    component: ComponentCreator('/mcp-workshop/blog/tags', 'e9e'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/tags/docusaurus',
    component: ComponentCreator('/mcp-workshop/blog/tags/docusaurus', '315'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/tags/facebook',
    component: ComponentCreator('/mcp-workshop/blog/tags/facebook', 'a97'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/tags/hello',
    component: ComponentCreator('/mcp-workshop/blog/tags/hello', '871'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/tags/hola',
    component: ComponentCreator('/mcp-workshop/blog/tags/hola', 'f61'),
    exact: true
  },
  {
    path: '/mcp-workshop/blog/welcome',
    component: ComponentCreator('/mcp-workshop/blog/welcome', '5ed'),
    exact: true
  },
  {
    path: '/mcp-workshop/markdown-page',
    component: ComponentCreator('/mcp-workshop/markdown-page', '6f3'),
    exact: true
  },
  {
    path: '/mcp-workshop/docs',
    component: ComponentCreator('/mcp-workshop/docs', 'fb2'),
    routes: [
      {
        path: '/mcp-workshop/docs',
        component: ComponentCreator('/mcp-workshop/docs', 'd52'),
        routes: [
          {
            path: '/mcp-workshop/docs',
            component: ComponentCreator('/mcp-workshop/docs', '972'),
            routes: [
              {
                path: '/mcp-workshop/docs/category/mcp-concepts',
                component: ComponentCreator('/mcp-workshop/docs/category/mcp-concepts', '53e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/mcp-workshop/docs/mcp-concepts/client',
                component: ComponentCreator('/mcp-workshop/docs/mcp-concepts/client', '2f0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/mcp-workshop/docs/mcp-concepts/external',
                component: ComponentCreator('/mcp-workshop/docs/mcp-concepts/external', 'eba'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/mcp-workshop/docs/mcp-concepts/first-server',
                component: ComponentCreator('/mcp-workshop/docs/mcp-concepts/first-server', '03c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/mcp-workshop/docs/mcp-concepts/intro',
                component: ComponentCreator('/mcp-workshop/docs/mcp-concepts/intro', '9a4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/mcp-workshop/docs/mcp-concepts/llm-client',
                component: ComponentCreator('/mcp-workshop/docs/mcp-concepts/llm-client', '06f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/mcp-workshop/docs/mcp-concepts/more',
                component: ComponentCreator('/mcp-workshop/docs/mcp-concepts/more', '21e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/mcp-workshop/docs/mcp-concepts/sse',
                component: ComponentCreator('/mcp-workshop/docs/mcp-concepts/sse', 'a0e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/mcp-workshop/docs/mcp-concepts/vscode',
                component: ComponentCreator('/mcp-workshop/docs/mcp-concepts/vscode', '87f'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/mcp-workshop/',
    component: ComponentCreator('/mcp-workshop/', 'a43'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
