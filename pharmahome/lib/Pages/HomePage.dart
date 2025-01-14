import 'package:flutter/material.dart';


class HomePage extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('PharmaHome'),
        leading: Builder(
          builder: (context) => IconButton(
            icon: Icon(Icons.menu),
            onPressed: () => Scaffold.of(context).openDrawer(),
          ),
        ),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
              child: Text(
                'Menu',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
            ),
            ListTile(
              leading: Icon(Icons.home),
              title: Text('Accueil'),
              onTap: () {
                // Action when this menu item is tapped
              },
            ),
            ListTile(
              leading: Icon(Icons.category),
              title: Text('Catégories'),
              onTap: () {
                // Action when this menu item is tapped
              },
            ),
            ListTile(
              leading: Icon(Icons.book),
              title: Text('Conseil'),
              onTap: () {
                // Action when this menu item is tapped
              },
            ),
            // Add more ListTile widgets here for more menu items
          ],
        ),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            SectionTitle(title: 'Produits Favoris'),
            FavoriteProductsCarousel(),
            SectionTitle(title: 'Catégories'),
            ProductCategories(),
          ],
        ),
      ),
    );
  }
}

class SectionTitle extends StatelessWidget {
  final String title;

  SectionTitle({required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}

class FavoriteProductsCarousel extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      child: ListView(
        scrollDirection: Axis.horizontal,
        children: <Widget>[
          ProductCard(),
          ProductCard(),
          ProductCard(),
          // Add more ProductCard widgets here
        ],
      ),
    );
  }
}

class ProductCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      margin: EdgeInsets.all(8.0),
      color: Colors.blueAccent,
      child: Center(
        child: Text(
          'Produit',
          style: TextStyle(color: Colors.white),
        ),
      ),
    );
  }
}

class ProductCategories extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        CategoryCard(),
        CategoryCard(),
        CategoryCard(),
        // Add more CategoryCard widgets here
      ],
    );
  }
}

class CategoryCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.all(8.0),
      padding: EdgeInsets.all(16.0),
      color: Colors.greenAccent,
      child: Row(
        children: <Widget>[
          Icon(Icons.category),
          SizedBox(width: 8.0),
          Text('Catégorie'),
        ],
      ),
    );
  }
}
