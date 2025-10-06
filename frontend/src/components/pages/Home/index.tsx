import "./index.scss";
import Card from "../../utilities/Card";
import { useEffect } from "react";
import { getProducts } from "../../../lib/requestUtils";
import { useQuery } from "@tanstack/react-query";
import { fetchData } from "../../../composables/api";

export default function Home() {
  const { data: products, isLoading: loadingProducts } = useQuery({
    queryKey: ['products', 'all'],
    queryFn: getProducts,
    staleTime: Infinity
  })
  useEffect(() => {

    fetchData("categories")
      .then((res) => res.json())
      .then(data => {
        console.log(data)
      })


  }, [])




  return <>
    <section className="carousel">


      <ul className="carousel-list">
        <li className="carousel-li">
          <section className="carousel-item">
            <div className="carousel-image"><img src="/dummies/banner-image-2.jpg" alt="" /></div>
            <div className="carousel-copy">
              <h2 className="carousel-title"><a href="/products/2021">Bananas</a></h2>
              <p className="carousel-p">Lorem, ipsum dolor sit amet consectetur adipisicing elit. Facere, debitis? Earum aliquid porro illo minima ipsum molestias corporis, delectus laudantium officia veritatis rem nulla vero dolores totam amet, id eum.</p>
              <button className="carousel-btn" data-btn>Add to Cart</button>
            </div>
          </section>
        </li>



        <li className="carousel-li">
          <section className="carousel-item">
            <div className="carousel-image"><img src="/dummies/singel-product-item.jpg" alt="" /></div>
            <div className="carousel-copy">
              <h2 className="carousel-title"><a href="/products/2021">Bananas</a></h2>
              <p className="carousel-p">Lorem, ipsum dolor sit amet consectetur adipisicing elit. Facere, debitis? Earum aliquid porro illo minima ipsum molestias corporis, delectus laudantium officia veritatis rem nulla vero dolores totam amet, id eum.</p>
              <button className="carousel-btn" data-btn>Add to Cart</button>
            </div>
          </section>
        </li>



        <li className="carousel-li">
          <section className="carousel-item">
            <div className="carousel-image"><img src="/dummies/post-thumb-1.jpg" alt="" /></div>
            <div className="carousel-copy">
              <h2 className="carousel-title"><a href="/products/2021">Bananas</a></h2>
              <p className="carousel-p">Lorem, ipsum dolor sit amet consectetur adipisicing elit. Facere, debitis? Earum aliquid porro illo minima ipsum molestias corporis, delectus laudantium officia veritatis rem nulla vero dolores totam amet, id eum.</p>
              <button className="carousel-btn" data-btn>Add to Cart</button>
            </div>
          </section>
        </li>


        <li className="carousel-li">
          <section className="carousel-item">
            <div className="carousel-image"><img src="/dummies/slide-1.jpg" alt="" /></div>
            <div className="carousel-copy">
              <h2 className="carousel-title"><a href="/products/2021">Bananas</a></h2>
              <p className="carousel-p">Lorem, ipsum dolor sit amet consectetur adipisicing elit. Facere, debitis? Earum aliquid porro illo minima ipsum molestias corporis, delectus laudantium officia veritatis rem nulla vero dolores totam amet, id eum.</p>
              <button className="carousel-btn" data-btn>Add to Cart</button>
            </div>
          </section>
        </li>
      </ul>



    </section>



    <section className="products">
      <h2 className="products-title">Trending Products</h2>


      <ul className="products-list">
        {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
         loadingProducts ? "Loading" : products?.map((product: any) => {
          return <li className="products-li" key={product.id}><Card productData={product}/></li>
        }) }
        
        {/* <li className="products-li"><Card /></li>
        <li className="products-li"><Card /></li>
        <li className="products-li"><Card /></li> */}
      </ul>
    </section>
  </>


}

